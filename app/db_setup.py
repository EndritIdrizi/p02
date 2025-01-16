'''
Team JBEE: Ben Rudinski, Vedant Kothari, Endrit Idrizi, Ziyad Hamed
SoftDev
P02
2025-01-08
Time Spent: 1
'''

import sqlite3
from config import Config

def setup_database(db_file=Config.DATABASE):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create games table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            pairs TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            difficulty TEXT,
            type TEXT,
            FOREIGN KEY(author_id) REFERENCES users(id)
        )
    ''')

    # Create user_games table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            status TEXT NOT NULL,  -- e.g., 'won' or 'lost'
            attempts INTEGER,
            time_spent REAL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(game_id) REFERENCES games(id)
        )
    ''')

    # Create statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_type TEXT NOT NULL,
            games_played INTEGER DEFAULT 0,
            won_first_attempt INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
