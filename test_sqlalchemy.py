from datetime import timedelta
from flask import Flask, request, jsonify
from collections.abc import Mapping
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret_key'
jwt = JWTManager(app)

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}')>"
    
    def to_dict(self):
        return {'id': self.id, 'username': self.username}

DATABASE_URL = 'postgresql+psycopg2://postgres:Dimalera0805@localhost:5432/db_for_users'
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/users')
def show_all_users():
    all_users = session.query(User).all()
    user_list = [user.to_dict() for user in all_users]
    return jsonify(user_list)

@app.route('/register', methods=['POST'])
def user_sign_in():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return jsonify({"msg": "Username or Password are required!"})
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    session.commit()
    return jsonify({"msg": "User added succesfully!"}), 200

@app.route('/login', methods=['POST'])
def user_sign_up():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return jsonify({"msg": "Username or Password are required!"})
    expires=timedelta(days=3)
    logged_user = session.query(User).filter(User.username == username).first()
    if logged_user and check_password_hash(logged_user.password, password):
        token = create_access_token(identity=logged_user.id, expires_delta=expires)
        return jsonify(token)
    else:
        return jsonify({"msg": "Username or password isn't valid!"})
    
@app.route('/protected')
@jwt_required()
def protected_get():
    return jsonify({"msg": "Successfully Authorizated!"})

if __name__ == '__main__':
    app.run(debug=True)