import eventlet
eventlet.monkey_patch()
import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='eventlet')

# In-memory storage for simplicity
questions = {}
answers = {}
admin_status = {}

class Question(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    question_text = db.Column(db.String(1000), nullable=False)
    time_stamp = db.Column(db.String(500), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    answer_text = db.Column(db.String(500))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(36), db.ForeignKey('question.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_question', methods=['POST'])
def submit_question():
    ip_add = request.remote_addr
    timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    question_text = request.form['question']
    question_id = str(uuid.uuid4())
    new_question = Question(id=question_id, ip=str(ip_add), time_stamp=str(timestamp), question_text=question_text)
    db.session.add(new_question)
    db.session.commit()
    admin_status[question_id] = False
    return redirect(url_for('personal_link', question_id=question_id))

@app.route('/personal_link/<question_id>')
def personal_link(question_id):
    link = request.url_root + 'chat/' + question_id
    return render_template('personal_link.html', link=link)

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

@app.route('/admin_page', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Incorrect password, please try again.')
            return render_template('login.html', error="Incorrect password, please try again.")
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'admin_logged_in' in session:
        all_questions = Question.query.all()
        return render_template('admin.html', questions=all_questions)
    else:
        return redirect(url_for('login'))

@app.route('/answer/<question_id>', methods=['GET', 'POST'])
def answer(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question.answer_text = request.form['answer']
        db.session.commit()
        flash('Answer submitted successfully', 'success')
        return redirect(url_for('admin'))
    return render_template('answer.html', question_id=question_id, question=question.question_text)

@app.route('/chat/<question_id>')
def chat(question_id):
    is_admin = request.args.get('admin', 'false').lower() == 'true'
    question = Question.query.get_or_404(question_id)
    messages = Message.query.filter_by(question_id=question_id).order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', question_id=question_id, question=question.question_text, is_admin=is_admin, messages=messages)

@socketio.on('join')
def handle_join(data):
    question_id = data['question_id']
    username = data['username']
    join_room(question_id)
    if username == 'admin':
        admin_status[question_id] = True
        emit('admin_status', {'admin_joined': True}, to=question_id)
    message = f"{username} has entered the room for question {question_id}."
    send({'msg': message, 'username': 'System', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, to=question_id)

@socketio.on('leave')
def handle_leave(data):
    question_id = data['question_id']
    username = data['username']
    leave_room(question_id)
    if username == 'admin':
        admin_status[question_id] = False
        emit('admin_status', {'admin_joined': False}, to=question_id)
    message = f"{username} has left the room for question {question_id}."
    send({'msg': message, 'username': 'System', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, to=question_id)

@socketio.on('message')
def handle_message(data):
    question_id = data['question_id']
    msg = data['message']
    username = data['username']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_message = Message(question_id=question_id, username=username, timestamp=datetime.now(), message=msg)
    db.session.add(new_message)
    db.session.commit()
    send({'msg': msg, 'username': username, 'timestamp': timestamp}, to=question_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
