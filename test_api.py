import requests
import json

BASE_URL = "http://localhost:5000"

def test_get_books():
    response = requests.get(f"{BASE_URL}/books")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_add_book(title, author, year):
    """Test adding a new book to the API"""
    new_book = {
        "title": title,
        "author": author,
        "year": year
    }
    response = requests.post(f"{BASE_URL}/books", json=new_book)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.json()

def test_delete_book(book_id):
    """Test deleting a book by ID"""
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.json()

def test_update_book(book_id, title=None, author=None, year=None):
    """Test updating a book's information"""
    update_data = {}
    if title:
        update_data["title"] = title
    if author:
        update_data["author"] = author
    if year:
        update_data["year"] = year
    
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.json()

def test_get_single_book(book_id):
    """Test getting a single book by ID"""
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.json()

if __name__ == "__main__":
    print("=" * 50)
    print("1. Testing GET all books (Initial state)")
    print("=" * 50)
    test_get_books()
    
    print("=" * 50)
    print("2. Testing ADD first book: 'The Hobbit'")
    print("=" * 50)
    book1 = test_add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    book1_id = book1.get("id")
    
    print("=" * 50)
    print("3. Testing ADD second book: 'Harry Potter'")
    print("=" * 50)
    book2 = test_add_book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1997)
    book2_id = book2.get("id")
    
    print("=" * 50)
    print("4. Testing GET all books (After adding 2 books)")
    print("=" * 50)
    test_get_books()
    
    print("=" * 50)
    print(f"5. Testing UPDATE book {book1_id} (The Hobbit - change year)")
    print("=" * 50)
    test_update_book(book1_id, year=1938)
    
    print("=" * 50)
    print(f"6. Testing GET single book {book1_id} (Verify update)")
    print("=" * 50)
    test_get_single_book(book1_id)
    
    print("=" * 50)
    print(f"7. Testing DELETE book {book2_id} (Harry Potter)")
    print("=" * 50)
    test_delete_book(book2_id)
    
    print("=" * 50)
    print("8. Testing GET all books (Final state)")
    print("=" * 50)
    test_get_books()
    
    print("=" * 50)
    print("All tests completed!")
    print("=" * 50)
    