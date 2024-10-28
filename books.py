from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

class Base(DeclarativeBase): pass

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    date = Column(String, nullable=False)
    genre = Column(String, nullable=False)

    def __repr__(self):
        return f"<Book(id = '{self.id}', name = '{self.name}', author = '{self.author}', date = '{self.date}', genre = '{self.genre}')>"
    
    def to_dict(self):
        return {'id':self.id, 'name':self.name, 'author':self.author, 
                'date':self.date, 'genre':self.genre}
    
DATABASE_URL = 'postgresql+psycopg2://postgres:Dimalera0805@localhost:5432/db_for_books'
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/book', methods=['POST'])
def create_book():
    name = request.form['name']
    author = request.form['author']
    date = request.form['date']
    genre = request.form['genre']
    new_book = Book(name = name, author = author, date = date, genre = genre)
    session.add(new_book)
    session.commit()
    return jsonify({"msg": "Book added succesfully!"}), 200

@app.route('/')
def all_books():
    all_books = session.query(Book).all()
    book_list = [book.to_dict() for book in all_books]
    return jsonify(book_list)

@app.route('/book')
def get_book():
    book_id = request.args.get('id', type=int)
    if book_id is None:
        return jsonify({"msg": "ID is required!"})
    book = session.query(Book).get(book_id)
    if book is None:
        return jsonify({"msg": "Book is not found!"})
    return jsonify(book.to_dict())

@app.route('/book', methods=['PUT'])
def update_book():
     name = request.form['name']
     author = request.form['author']
     date = request.form['date']
     genre = request.form['genre']
     book_id = request.args.get('id', type=int)
     if book_id is None:
        return jsonify({"msg": "ID is required!"})
     book = session.query(Book).get(book_id)
     if book is None:
        return jsonify({"msg": "Book is not found!"})
     book.name = name
     book.author = author
     book.date = date
     book.genre = genre
     session.add(book)
     session.commit()
     return jsonify({"msg": "Book updated succesfully!"}), 200

@app.route('/book', methods=['DELETE'])
def delete_book():
     book_id = request.args.get('id', type=int)
     if book_id is None:
        return jsonify({"msg": "ID is required!"})
     book = session.query(Book).get(book_id)
     if book is None:
        return jsonify({"msg": "Book is not found!"})
     session.delete(book)
     session.commit()
     return jsonify({"msg": "Book deleted succesfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    
