import psycopg2
from psycopg2.extras import DictCursor
from datetime import timedelta
from flask import Flask, request, jsonify
from collections.abc import Mapping
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt = JWTManager(app)

conn = psycopg2.connect(dbname="postgres", user="postgres", password="Dimalera0805", host="127.0.0.1", port="5432", options="-c client_encoding=UTF8")
cursor=conn.cursor(cursor_factory=DictCursor)

cursor.execute('''
        CREATE TABLE IF NOT EXISTS userss (
            id SERIAL PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            password VARCHAR NOT NULL
        )
    ''')
conn.commit()


@app.route('/users')
def all_users():
    cursor.execute("SELECT * FROM userss")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/register', methods = ['POST'])
def user_sign_in():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return jsonify({"msg": "Username or Password are required!"})
    cursor.execute("SELECT COUNT (*) FROM userss WHERE username = %s", (username,))
    count = cursor.fetchone()[0]
    if count > 0:
        return jsonify({"msg": "User already exist!"})
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO userss (username, password) VALUES (%s, %s)", (username, hashed_password,))
    conn.commit()
    return jsonify ({"message": "User registered succesfully!"}), 200

@app.route('/login', methods = ['POST'])
def user_sign_up():
    username = request.form['username']
    password = request.form['password']
    
    expires = timedelta(days=3)
    cursor.execute("SELECT * FROM userss WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user and check_password_hash(user['password'], password):
        token = create_access_token(identity=user['id'], expires_delta=expires)
        return jsonify(token)
    else:
        return jsonify({"msg": "Username or Password isn't valid"})

@app.route('/protected', methods = ['GET'])
@jwt_required()
def protected_get():
    return jsonify({"message": "This is a protected route!"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
 
