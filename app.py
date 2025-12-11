from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

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

# Initialize database on startup
if not os.path.exists(DATABASE):
    init_db()

@app.route('/')
def home():
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
    return jsonify({"books": books_list, "count": len(books_list)})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book:
        return jsonify(dict(book))
    return jsonify({"error": "Book not found"}), 404

@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not all(k in request.json for k in ['title', 'author', 'year']):
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
    return jsonify(dict(new_book)), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if not book:
        conn.close()
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
    return jsonify(dict(updated_book))

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404
    
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)