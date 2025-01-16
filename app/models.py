'''
Team JBEE: Ben Rudinski, Vedant Kothari, Endrit Idrizi, Ziyad Hamed
SoftDev
P02
2025-01-08
Time Spent: 2
'''

# models.py

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

# class for db with basic methods
class Database:
    # establish a connection with db
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(current_app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        return conn

class User:
    # get our user by ID very straightforward
    @staticmethod
    def get_by_id(user_id):
        conn = Database.get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return user

    # get user by username
    @staticmethod
    def get_by_username(username):
        conn = Database.get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return user

    # create a user
    @staticmethod
    def create(username, password):
        password_hash = generate_password_hash(password)
        conn = Database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()

    # verify their password via hashes
    @staticmethod
    def verify_password(stored_hash, password):
        return check_password_hash(stored_hash, password)

# CLASS for an actual game of connections or wordle
class Game:
    # create a game by difficulty, etc
    @staticmethod
    def create(title, pairs, author_id, difficulty, game_type):
        conn = Database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (title, pairs, author_id, difficulty, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, pairs, author_id, difficulty, game_type))
        conn.commit()
        conn.close()

    # get aall games avaialble
    @staticmethod
    def get_all():
        conn = Database.get_db_connection()
        games = conn.execute('SELECT * FROM games').fetchall()
        conn.close()
        return games

    # fetch a certain gae by id
    @staticmethod
    def get_by_id(game_id):
        conn = Database.get_db_connection()
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()[0]
        conn.close()
        return game

class UserGame:
    # create a game.
    @staticmethod
    def create(user_id, game_id, type, status, attempts, time_spent):
        conn = Database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_games (user_id, game_id, status, attempts, time_spent)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, game_id, status, attempts, time_spent))
        conn.commit()
        conn.close()
    # find which user made the game
    @staticmethod
    def get_by_user(user_id):
        conn = Database.get_db_connection()
        user_games = conn.execute('''
            SELECT ug.*, g.title, g.type
            FROM user_games ug
            JOIN games g ON ug.game_id = g.id
            WHERE ug.user_id = ?
        ''', (user_id,)).fetchall()
        conn.close()
        return user_games

# statistics potentially for more features, insteado f user settings
class Statistic:
    @staticmethod
    def create_if_not_exists(user_id, game_type):
        conn = Database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO statistics (user_id, game_type)
            VALUES (?, ?)
        ''', (user_id, game_type))
        conn.commit()
        conn.close()
        
    @staticmethod
    def update(user_id, game_type, won_on_first_attempt=False):
        conn = Database.get_db_connection()
        cursor = conn.cursor()
        if won_on_first_attempt:
            cursor.execute('''
                UPDATE statistics
                SET games_played = games_played + 1,
                    won_first_attempt = won_first_attempt + 1
                WHERE user_id = ? AND game_type = ?
            ''', (user_id, game_type))
        else:
            cursor.execute('''
                UPDATE statistics
                SET games_played = games_played + 1
                WHERE user_id = ? AND game_type = ?
            ''', (user_id, game_type))
        conn.commit()
        conn.close()
