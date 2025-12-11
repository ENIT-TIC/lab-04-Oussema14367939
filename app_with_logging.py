from flask import Flask, jsonify, request
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import sqlite3

app = Flask(__name__)

# Configuration du logging
log_dir = '/app/logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'flask_api.log')

# Configuration du handler de fichier avec rotation
file_handler = RotatingFileHandler(log_file, maxBytes=10240000, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))

# Configuration du logger Flask
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Flask Books API startup')

# Database configuration
DATABASE = '/app/data/books.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with schema"""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = get_db_connection()
    with open('/app/init_db.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    app.logger.info('Database initialized successfully')

# Initialize database on startup
if not os.path.exists(DATABASE):
    init_db()

@app.route('/')
def home():
    app.logger.info('Home endpoint accessed')
    return jsonify({
        "message": "Welcome to the Books API",
        "version": "1.0",
        "endpoints": {
            "GET /books": "List all books",
            "GET /books/<id>": "Get a specific book",
            "POST /books": "Add a new book",
            "PUT /books/<id>": "Update a book",
            "DELETE /books/<id>": "Delete a book",
            "GET /health": "Health check"
        }
    })

@app.route('/health')
def health():
    app.logger.info('Health check endpoint accessed')
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    books_list = [dict(book) for book in books]
    app.logger.info(f'GET all books - Total: {len(books_list)}')
    return jsonify({"books": books_list, "count": len(books_list)})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    app.logger.info(f'GET book with id: {book_id}')
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book:
        app.logger.info(f'Book found: {book["title"]}')
        return jsonify(dict(book))
    app.logger.warning(f'Book not found with id: {book_id}')
    return jsonify({"error": "Book not found"}), 404

@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not all(k in request.json for k in ['title', 'author', 'year']):
        app.logger.error('POST book failed - Missing required fields')
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
        (request.json['title'], request.json['author'], request.json['year'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    new_book = conn.execute('SELECT * FROM books WHERE id = ?', (new_id,)).fetchone()
    conn.close()
    app.logger.info(f'POST new book - ID: {new_id}, Title: {request.json["title"]}')
    return jsonify(dict(new_book)), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    app.logger.info(f'PUT update book with id: {book_id}')
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if not book:
        conn.close()
        app.logger.warning(f'PUT failed - Book not found with id: {book_id}')
        return jsonify({"error": "Book not found"}), 404
    
    if request.json:
        updates = []
        values = []
        for key in ['title', 'author', 'year']:
            if key in request.json:
                updates.append(f'{key} = ?')
                values.append(request.json[key])
        
        if updates:
            values.append(book_id)
            conn.execute(f'UPDATE books SET {", ".join(updates)} WHERE id = ?', values)
            conn.commit()
    
    updated_book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    app.logger.info(f'PUT book updated - ID: {book_id}, New data: {dict(updated_book)}')
    return jsonify(dict(updated_book))

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    app.logger.info(f'DELETE book with id: {book_id}')
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if not book:
        conn.close()
        app.logger.warning(f'DELETE failed - Book not found with id: {book_id}')
        return jsonify({"error": "Book not found"}), 404
    
    book_title = book["title"]
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    app.logger.info(f'DELETE successful - Book deleted: {book_title}')
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
