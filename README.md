# Anonymous Confession App with Personalized Chat Room
This is a Ask/Confession & chat application built with Flask, SocketIO, and SQLAlchemy. The application allows users to be anonymous to the admin, submit questions and receive answers from an admin through a real-time chat interface.


---

⚠️ **Warning: Not for Production Use**

This application is intended for educational and experimental purposes only. It is not designed or tested for production environments.

---
## Features

- Submit anonymous confessions with unique chat links
- Admin login to answer questions.
- Real-time chat functionality using SocketIO.
- Persistent storage of questions and messages using SQLAlchemy.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Mayukh-Mondal-Dev/Private-Confession-App
    cd Private-Confession-App
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5000`.
2. Submit a question and receive a unique chat link.
3. Admin can login using the `/admin_page` route and answer questions.
4. Use the chat link to join the real-time chat for the submitted question.

## Configuration

- Modify the `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` in the `app.py` file to fit your needs.
- Set the admin password in the `ADMIN_PASSWORD` variable in `.env`.

## Project Structure

```plaintext
Private-Confession-App/
│
├── app.py
├── .env
├── requirements.txt        
├── templates/              
│   ├── index.html
│   ├── login.html
│   ├── admin.html
│   ├── answer.html
│   ├── chat.html
│   └── personal_link.html
├── static/
│   └── style.css
└── README.md               
```

## License

This project is licensed under the <b>GNU General Public License version 3 (GPLv3)</b>. See the LICENSE file for more details.

## Contributing

Feel free to open issues or submit pull requests for any improvements or bug fixes.

---
