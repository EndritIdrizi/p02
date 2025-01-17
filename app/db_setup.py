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
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL
        );
    ''')

    # Create wordle table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, name TEXT, 
            description TEXT,
            word TEXT
        )
    ''')

    # Create games table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            pairs TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            type TEXT NOT NULL, -- "wordle" or "connections"
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')

    # Create user_games table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            result TEXT NOT NULL, -- "won" or "lost"
            attempts INTEGER NOT NULL,
            time_spent REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(game_id) REFERENCES games(id)
        );
    ''')

    # Create statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_type TEXT NOT NULL, -- "Wordle" or "Connections"
            games_played INTEGER NOT NULL DEFAULT 0,
            won_first_attempt INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id),
            UNIQUE(user_id, game_type)
        );
    ''')

    # Create completed_groups table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            group_name TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(game_id) REFERENCES games(id)
        );
    ''')
    
    # Create wordle table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, name TEXT, 
            description TEXT,
            word TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
