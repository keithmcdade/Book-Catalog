from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from catalog.auth import login_required
from catalog.db import get_db
import catalog.config
import requests
import json


bp = Blueprint('dashboard', __name__)
# API key not included, get your own!
API_key = catalog.config.api_key


# shows user book catalog
@bp.route('/')
def index():
    
    if session.get('user_id'):
        
        user_id = int(session.get('user_id'))
        print(user_id)
        sql = 'SELECT * FROM books WHERE user_id=?;'
        db = get_db()
        books = db.execute(sql, (user_id,)).fetchall()
        return render_template('dashboard/index.html', books=books) 
    
    else:
        return render_template('dashboard/index.html')
        

# deletes book from catalog when 'delete' button is clicked
@bp.route('/delete', methods=['GET', 'POST'])
def delete():
    
    if request.method == "POST":
        user_id = int(session.get('user_id'))
        print(user_id)
        isbn = int(request.args['isbn'])
        sql = 'DELETE FROM books WHERE isbn=? AND user_id=?;'
        db = get_db()
        db.execute(sql, (isbn, user_id))
        db.commit()
        return redirect('/')
    
    else:
        return redirect('/')


# handles passing search query value to functions 
# for searching Google Books and parsing json 
# then displaying result on /search page
@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    
    if request.method == 'POST':
        query = request.form['search']
        book_data = get_volumeInfo(query)
        
        if not book_data:
            flash(f'No results for "{query}"')
            return render_template('dashboard/search.html')    

        book_info = get_book_info(book_data)
        book = Book(*book_info)
        
        return render_template('dashboard/search.html', query=query, book=book)                 
    
    else:
        return render_template('dashboard/search.html')


# adds book when "add" button on /search page is clicked
@bp.route('/search/add', methods=('GET', 'POST'))
def catalog_book():
    
    if request.method == "POST":
        isbn = int(request.args['isbn'])
        user_id = int(session.get('user_id'))
        
        if book_exists(isbn):
            flash('That book was already registed in your catalog')
            return render_template('dashboard/search.html')

        # use isbn from search to add book from Book instances
        for book in Book.books:
            if isbn == book.isbn and user_id == book.user_id:
                add_book(book)
                return redirect('/')
            

# book class for easier handling of books between views
class Book():
    
    books = []
    
    def __init__(self, isbn, title, authors, page_count, rating, user_id):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.page_count = page_count
        self.rating = rating
        self.user_id = user_id    
        Book.books.append(self)
        

# following functions for handling book database
#  --
# get_books gets books table from sql database for dashboard/index
def get_books():
    
    db = get_db
    sql = '''SELECT *
             FROM books'''
    return db.execute(sql).fetchall()
     

# add_book inserts book into sql database
def add_book(book):
    
    db = get_db()
    sql = 'INSERT INTO books (isbn, title, author, page_count, rating, user_id) VALUES (?, ?, ?, ?, ?, ?);'
    book_info = (book.isbn,
                 book.title,
                 book.authors,
                 book.page_count,
                 book.rating,
                 book.user_id)
    db.execute(sql, book_info)
    db.commit()       


# book_exists checks sql database by isbn, 
# returns bool on whether book is already cataloged 
def book_exists(isbn):
    
    user_id = int(session.get('user_id'))
    db = get_db()
    sql = 'SELECT * FROM books WHERE user_id=?;'
    books = db.execute(sql, (user_id,)).fetchall()
    for book in books:
        if book['isbn'] == isbn:
            return True
        else:
            return False
        

# calls functions for calling functions for getting 
# required book info and returning it as a list
def get_book_info(book_data):
    user_id = int(session.get('user_id'))
    return (get_isbn(book_data), 
            book_data['title'], 
            get_authors(book_data['authors']),
            get_pageCount(book_data), 
            None,
            user_id)  
                

# following functions process json from Google Books API
# --
# get_volumeInfo extracts volumeInfo value from json
def get_volumeInfo(query):
    
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{query}&key={API_key}"
        
    try:
        url_response = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"  

    json_response = url_response.text
    json_data = json.loads(json_response)
    
    if int(json_data['totalItems']) == 0:        
        return False
    
    book_data = json_data['items'][0]['volumeInfo']
    return book_data


# get_isbn returns book isbn, currently only supports isbn 13
def get_isbn(book_data):
    
    for item in book_data['industryIdentifiers']:
        if item['type'] == "ISBN_13":
            return int(item['identifier'])
        

# get_pageCount returns book's page count
def get_pageCount(book_data):
    
    if book_data.get('pageCount'):
        return book_data['pageCount']
    else:
        return None


# get_authors returns authors. 
def get_authors(author_list):    
    
    authors = ""
    
    # author_list is str if there is only 1 author
    # returns author_list with no change  
    if author_list == str:
        return author_list
    
    # if more than 1 author, author_list is a list
    # escapes recursion if author_list is empty
    if not author_list:
        return authors
    
    # recursion function for creating string from list
    if len(author_list) == 1:
        return authors + (author_list.pop(0) + get_authors(author_list))
    else:
        return authors + (author_list.pop(0) + ", " + get_authors(author_list)) 
       