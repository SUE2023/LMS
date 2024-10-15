#!/usr/bin/env python3
""" objects that handle all default RestFul API actions for Users """
from models.User import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
# Managing Users (Admins or Staff): handles user creation, login, and role-based access

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        """Collect data from form"""
        username = request.form['username']
        password = request.form['password']
        # Create and save user
        new_user = User(username=username)
        new_user.set_password(password)  # bcrypt or hashing logic
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!')
        return redirect(url_for('login'))
    return render_template('user/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        """Authentication logic"""
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
    return render_template('user/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
