import sqlite3

db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

def setup():
    userTable()
    gameTable()

def userTable():
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    db.commit()

def gameTable():
    cursor.execute('''
        CREATE TABLE games(id INTEGER PRIMARY KEY, TEXT user_id, INTEGER status, TEXT type, INTEGER attempts, FLOAT time_spent)
        ''')
    db.commit()
