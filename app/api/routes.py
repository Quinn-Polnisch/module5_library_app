from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# adding a book
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    publisher = request.json['publisher']
    length = request.json['length']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, title, author, publisher, length, user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# all books
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# single book
@api.route('/books/<isbn>', methods = ['GET'])
@token_required
def get_book(current_user_token, isbn):
    book = Book.query.get(isbn)
    response = book_schema.dump(book)
    return jsonify(response)

# update endpoint
@api.route('/books/<isbn>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, isbn):
    book = Book.query.get(isbn)
    book.isbn = request.json['isbn']
    book.title = request.json['title']
    book.author = request.json['author']
    book.publisher = request.json['publisher']
    book.length = request.json['length']
    current_user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# remove endpoint
@api.route('/books/<isbn>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, isbn):
    book = Book.query.get(isbn)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)