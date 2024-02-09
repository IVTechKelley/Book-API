"""
Title: Book REST API

Author: Patrick Kelley

Description: A simple Flask API for managing books with SQLite database.

How to Use:
    1. Install flask, python-dotenv, requests, and flask-sqlalchemy
    2. In the terminal, enter > flask init-db
    3. Run the program
    4. Use the terminal or a system like Postman to add or delete entries in the database.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# Define the Book model for the database
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))


# Flask CLI command to initialize the database
@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()


# Route to display a welcome message
@app.route('/')
def index():
    return 'Hello!'


# Route to get a list of all books
@app.route('/books')
def get_books():
    # Query all books from the database
    books = Book.query.all()
    # Format the books data for JSON response
    output = [{'name': book.name, 'author': book.author, 'publisher': book.publisher} for book in books]
    return jsonify({"books": output})


# Route to get details of a specific book by ID
@app.route('/books/<id>')
def get_book(id):
    # Query a specific book by ID or return a 404 error if not found
    book = Book.query.get_or_404(id)
    return {"name": book.name, "author": book.author, 'publisher': book.publisher}


# Route to add a new book to the database
@app.route('/books', methods=['POST'])
def add_book():
    # Extract JSON data from the request
    data = request.json
    # Create a new Book object and add it to the database
    book = Book(name=data['name'], author=data['author'], publisher=data['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}


# Route to delete a book by ID
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    # Query a specific book by ID
    book = Book.query.get(id)
    # Check if the book exists, if not, return an error
    if book is None:
        return {"error": "not found"}
    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()
    return {"message": "Success"}


# Run the Flask application on port 8000 in debug mode
if __name__ == '__main__':
    app.run(debug=True, port=8000)
