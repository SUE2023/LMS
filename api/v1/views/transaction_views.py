#!/usr/bin/env python3
""" objects that handle all default RestFul API actions for Books """
from models.Book import Book, BookDetails
from models.Member import Member
from models.Transaction import Transaction
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from flask import render_template, redirect, url_for, flash, request

# Managing Transactions (Issue/Return) : handles issuing and returning books to/from members.

@app.route('/transactions', methods=['GET'])
def view_transactions():
    """Retrives all transactions of the daqy"""
    transactions = Transaction.query.all()
    return render_template('transaction/transactions.html', transactions=transactions)

@app.route('/transactions/issue', methods=['GET', 'POST'])
def issue_book():
    """Updates books issued"""
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_id = request.form['book_id']
        new_transaction = Transaction(member_id=member_id, book_id=book_id, transaction_type='issue')
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for('view_transactions'))
    members = Member.query.all()
    books = Book.query.all()
    return render_template('transaction/issue_book.html', members=members, books=books)

@app.route('/transactions/return/<int:transaction_id>', methods=['POST'])
def return_book(transaction_id):
    """Updates returned books"""
    transaction = Transaction.query.get(transaction_id)
    transaction.transaction_type = 'return'
    db.session.commit()
    return redirect(url_for('view_transactions'))
