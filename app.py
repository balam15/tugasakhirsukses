import json
import sqlite3
from sqlite3 import Error
from flask import abort, Flask, jsonify, redirect, request, url_for

app = Flask(__name__)

def create_connection():
    try:
        return sqlite3.connect('CatarAction.db')
    except:
        print('Error! cannot create the database connection.')
        return None

def create_table():
    try:
        with create_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id integer PRIMARY KEY,
                    username text NOT NULL,
                    email text NOT NULL,
                    password text NOT NULL
                );
            ''')
    except Error as e:
        print(e)

def register_akun():
    with create_connection() as conn:
        c = conn.cursor()

        if request.json:
            username = json.loads(
                request.data
            ).get('username')
            email = json.loads(
                request.data
            ).get('email')
            password = json.loads(
                request.data
            ).get('password')
        else:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

        if username and email and password:
            c.execute(
                '''
                    INSERT INTO users(username, email, password)
                                VALUES(?, ?, ?);
                ''',
                (username, email, password)
            )
            return {"Register": "Berhasil"}

        else:
            abort(400)
            return {"Register" : "Gagal"}

def login_akun():
    with create_connection() as conn:
        c = conn.cursor()

        if request.json:
            username = json.loads(request.data).get('username')
            password = json.loads(request.data).get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        if username and password:
            c.execute(
                '''
                    SELECT * FROM users WHERE username = ? AND password = ?;
                ''',
                (username, password)
            )
            result = c.fetchone()

            if result:
                ambil_id = result[0]
                return {"Login": "Success"}
            else:
                return {"Login": "Failed"}

        else:
            abort(400)
            return {"Login": "Failed"}

@app.route('/')
def home():
    return ('Hello Guys!')

@app.route('/register', methods=['POST'])
def register():
    data = register_akun()
    return jsonify(data)

@app.route('/login', methods=['POST'])
def login():
    data = login_akun()
    return jsonify(data)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
