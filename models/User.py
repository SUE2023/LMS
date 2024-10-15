#!/usr/bin/env python3
""" User model"""

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime, Integer, Float
from models.BaseModel import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import bcrypt

class User(BaseModel):
    """User class inheriting from BaseModel and representing a User"""
    
    if models.storage_t == "db":
        __tablename__ = 'User'
        id = Column(Integer, primary_key=True, autoincrement=True)
        first_name = Column(String(128), nullable=False)
        second_name = Column(String(128), nullable=False)
        password_hash = Column(String(256), nullable=False)
        registration_date = Column(DateTime, default=datetime.utcnow) 
        rented_books = Column(String, nullable=True)  # Ideally a relationship
    else:
        id = ""
        first_name = ""
        second_name = ""
        registration_date = "" 
        password_hash = ""
        rented_books = ""

    def register(self, first_name, second_name, password):
        """Registers a user of the application."""
        self.first_name = first_name
        self.second_name = second_name
        self.registration_date = datetime.utcnow()
        self.set_password(password)  # Set the password during registration
        models.storage.save(self)  # Assuming this is a method to save to the database
        return f"Registered user {self.id} on {self.registration_date}"

    # Hash the password
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Decode to store as a string

    # Check the password
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        # Encode the hashed password for comparison
    
    # Flask-Login required methods:
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
