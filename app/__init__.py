'''
Team JBEE: Ben Rudinski, Vedant Kothari, Endrit Idrizi, Ziyad Hamed
SoftDev
P02
2025-01-08
Time Spent: 0.5
'''

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config  # Ensure config.py is in the correct directory
from functools import wraps

# Flask app initialization
app = Flask(__name__)
app.config.from_object(Config)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'site.db')

# Database connection function
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to access this page. Please log in.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home route
@app.route('/')
def home():
    return "JBEE is the best"

