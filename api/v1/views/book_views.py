#!/usr/bin/env python3
""" objects that handle all default RestFul API actions for Books """
from models.Book import Book, BookDetails
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from flask import render_template, redirect, url_for, flash, request

# Managing Books and Book Details: handles adding books, listing books, and showing book details

@app.route('/books', methods=['GET'])
def list_books():
    """Lists all books"""
    books = Book.query.all()
    return render_template('book/books.html', books=books)

@app.route('/books/<int:book_id>', methods=['GET'])
def book_details(book_id):
    """Retrives books details"""
    book = Book.query.get(book_id)
    details = BookDetails.query.filter_by(book_id=book_id).first()
    return render_template('book/book_details.html', book=book, details=details)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    """Add new book to the Inventory"""
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        # Assuming BookDetails is added separately
        new_book = Book(title=title, author=author, genre=genre)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('list_books'))
    return render_template('book/add_book.html')
