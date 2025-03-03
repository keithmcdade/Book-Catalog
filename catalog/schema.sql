CREATE TABLE users (
    user_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL
);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY NOT NULL,
    isbn INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    page_count INTEGER,
    rating INTEGER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id) 
);

INSERT INTO books (isbn, title, author, page_count, user_id) VALUES (9781449355715, "Learning Python", "Mark Lutz", 1645, 1);
