'''
Team JBEE: Ben Rudinski, Vedant Kothari, Endrit Idrizi, Ziyad Hamed
SoftDev
P02
2025-01-08
Time Spent: 0.5
'''

import os

DB_FILE = os.path.join(os.path.dirname(__file__), "site.db")

def read_key(keys_dir, file_name):
    key_path = os.path.join(keys_dir, file_name)
    try:
        with open(key_path, 'r') as key_file:
            return key_file.read().strip()
    except FileNotFoundError:
        print(f"Oh no! {file_name} not found in {keys_dir}.")  # displays error message if not found
        return None

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'PookieBear1' # we might change later

    # keys directory
    KEYS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'keys')

    # API keys (to add in future)

    # db configuration
    DATABASE = DB_FILE