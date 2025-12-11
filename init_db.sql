-- Create books table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);

-- Insert initial data
INSERT INTO books (title, author, year) VALUES
    ('1984', 'George Orwell', 1949),
    ('To Kill a Mockingbird', 'Harper Lee', 1960),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925);
