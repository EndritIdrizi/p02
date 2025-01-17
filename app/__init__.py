'''
Team JBEE: Ben Rudinski, Vedant Kothari, Endrit Idrizi, Ziyad Hamed
SoftDev
P02
2025-01-08
Time Spent: 3
'''

import os, sys
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from functools import wraps
from werkzeug.utils import secure_filename
import requests
import time
from models import User, Game, UserGame, Statistic, Database, CompletedGroup, generate_password_hash
import config

# adding config.py to search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Flask app initialization
app = Flask(__name__)
app.config.from_object(config.Config)

# make sure the database tables are set up
from db_setup import setup_database
setup_database(app.config['DATABASE'])

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
@app.route('/') # home page route
@login_required
def home():
    user = None
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])

    return render_template(
        'homepage.html'
    )

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # retrieve form data
        username = request.form.get('username').strip()
        password = request.form.get('password')

        # server-side validation
        if not username or not password:
            flash("all fields are required.", "danger")
            return redirect(url_for('login'))

        # fetch user from the database
        user = User.get_by_username(username)
        if user and User.verify_password(user['password_hash'], password):
            session['user_id'] = user['id']
            flash("logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        username = request.form.get('username').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not name or not username or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return redirect(url_for('register'))
        
        if username.startswith(' '):
            flash("Username cannot start with a space.", "danger")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        if len(password) < 12:
            flash("Password must be at least 12 characters long.", "danger")
            return redirect(url_for('register'))

        if not any(c.islower() for c in password):
            flash("Password must contain at least one lowercase letter.", "danger")
            return redirect(url_for('register'))

        if not any(c.isupper() for c in password):
            flash("Password must contain at least one uppercase letter.", "danger")
            return redirect(url_for('register'))

        if not any(c.isdigit() for c in password):
            flash("Password must contain at least one number.", "danger")
            return redirect(url_for('register'))

        # check if username already exists
        existing_user = User.get_by_username(username)
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('register'))

        # hash the password
        hashed_password = generate_password_hash(password)

        # create user
        try:
            User.create(username, hashed_password, name)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for('register'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('home'))

@app.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    if request.method == 'POST':
        title = request.form.get('title')
        pairs = request.form.get('pairs')
        difficulty = request.form.get('difficulty')
        game_type = request.form.get('type')

        # val
        if not title:
            flash("No Title!", "danger")
            return redirect(url_for('create_game'))
        if not pairs or ';' not in pairs:
            flash("Invalid pairs format. Format it like group1;group2;group3;group4", "danger")
            return redirect(url_for('create_game'))
        if not difficulty:
            flash("Difficulty level is required.", "danger")
            return redirect(url_for('create_game'))
        if not game_type:
            flash("Game type is required.", "danger")
            return redirect(url_for('create_game'))
    
        Game.create(title, pairs, session['user_id'], difficulty, game_type)
        flash("Game created successfully!", "Success")
        return redirect(url_for('home'))
    return render_template('create.html')

# create connections route
@app.route('/create/connections', methods=['GET', 'POST'])
@login_required
def create_connections():
    if request.method == 'POST':
        # retrieve form data for creating connections
        connection_name = request.form.get('connection_name').strip()
        connection_description = request.form.get('connection_description').strip()

        # server-side validation
        if not connection_name or not connection_description:
            flash("all fields are required to create a connection.", "danger")
            return redirect(url_for('create_connections'))

        # insert the new connection into the database
        try:
            conn = Database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO connections (user_id, name, description) VALUES (?, ?, ?)',
                (session['user_id'], connection_name, connection_description)
            )
            conn.commit()
            conn.close()
            flash("connection created successfully!", "success")
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            flash("an error occurred while creating the connection. please try again.", "danger")
            return redirect(url_for('create_connections'))

    return render_template('create_connections.html')

# create wordle route
@app.route('/create/wordle', methods=['GET', 'POST'])
@login_required
def create_wordle():
    if request.method == 'POST':
        # retrieve form data for creating wordle
        wordle_name = request.form.get('wordle_name').strip()
        wordle_description = request.form.get('wordle_description').strip()
        wordle_word = request.form.get('wordle_word').strip()

        # server-side validation
        if not wordle_name or not wordle_description or not wordle_word:
            flash("all fields are required to create a wordle.", "danger")
            return redirect(url_for('create_wordle'))

        if len(wordle_word) != 5 or not wordle_word.isalpha():
            flash("wordle word must be exactly 5 alphabetic characters.", "danger")
            return redirect(url_for('create_wordle'))

        # insert the new wordle into the database
        try:
            conn = Database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO wordles (user_id, name, description, word) VALUES (?, ?, ?, ?)',
                (session['user_id'], wordle_name, wordle_description, wordle_word.lower())
            )
            conn.commit()
            conn.close()
            flash("wordle created successfully!", "success")
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            flash("an error occurred while creating the wordle. please try again.", "danger")
            return redirect(url_for('create_wordle'))

    return render_template('create_wordle.html')

# view your created games
@app.route('/my_games', methods=['GET', 'POST'])
@login_required
def my_games():
    games = Game.get_all()
    user_games = [game for game in games if game['author_id'] == session['user_id']]
    return render_template('my_games.html', games=user_games)

# play game
@app.route('/play/<int:game_id>', methods=['GET', 'POST'])
@login_required
def play_game(game_id):
    game = Game.get_by_id(game_id)
    if not game:
        flash("Game not found", "Danger")
        return redirect(url_for('home'))
    
    game_type = game['type'] 
    
    if game_type.lower() == 'wordle':
        return redirect(url_for('play_wordle', game_id=game_id))
    elif game_type.lower() == 'connections':
        return redirect(url_for('play_connections', game_id=game_id))
    else:
        flash("Incorrect game type!", "Danger")
        return redirect(url_for('home'))
    
# Play Wordle
@app.route('/play_wordle/<int:game_id>', methods=['GET', 'POST'])
@login_required
def play_wordle(game_id):
    game = Game.get_by_id(game_id)
    if not game:
        flash("Game not found.", "danger")
        return redirect(url_for('home'))

    # init game state in session if not present
    if 'wordle_game' not in session or session['wordle_game']['game_id'] != game_id:
        session['wordle_game'] = {
            'game_id': game_id,
            'attempts': 0,
            'max_attempts': 6,
            'saved_word': extract_saved_word(game['pairs']), 
            'guesses': [],
            'start_time': time.time()
        }

    if request.method == 'POST':
        user_guess = request.form.get('word').lower()

        # input validation
        if len(user_guess) != 5 or not user_guess.isalpha():
            flash("Please enter a valid 5-letter word (only letters allowed).", "danger")
            return redirect(url_for('play_wordle', game_id=game_id))

        # we need miriam web api
        api_key = app.config['MW_API_KEY']
        if not api_key:
            flash("Dictionary API key not configured.", "danger")
            return redirect(url_for('play_wordle', game_id=game_id))
        response = requests.get(
            f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{user_guess}",
            params={'key': api_key}
        )
        data = response.json()
        if not data or not isinstance(data, list) or not isinstance(data[0], dict):
            flash("Invalid word.", "danger")
            return redirect(url_for('play_wordle', game_id=game_id))

        # game logic
        saved_word = session['wordle_game']['saved_word']
        session['wordle_game']['attempts'] += 1

        # check if the guess is correct
        if user_guess == saved_word:
            flash("Congratulations! You guessed the word!", "success")
            # update user games and statistics
            UserGame.create(session['user_id'], game_id, 'won', session['wordle_game']['attempts'], time.time())
            Statistic.create_if_not_exists(session['user_id'], 'Wordle')
            Statistic.update(session['user_id'], 'Wordle', won_on_first_attempt=(session['wordle_game']['attempts'] == 1))
            # play congratulatory music
            music_files = get_congrats_music()
            return render_template('congrats.html', music_files=music_files)

        # add guess to guesses
        session['wordle_game']['guesses'].append(user_guess)

        if session['wordle_game']['attempts'] >= session['wordle_game']['max_attempts']:
            flash(f"Game Over! The correct word was '{saved_word}'.", "danger")
            # update user games and statistics
            time_spent = time.time() - session['wordle_game']['start_time']
            
            UserGame.create(session['user_id'], game_id, 'lost', session['wordle_game']['attempts'], time_spent)
            Statistic.create_if_not_exists(session['user_id'], 'Wordle')
            Statistic.update(session['user_id'], 'Wordle', won_on_first_attempt=False)
            return redirect(url_for('home'))

        flash("Keep trying!", "info")
        return redirect(url_for('play_wordle', game_id=game_id))

    # retrieve game state
    wordle_game = session.get('wordle_game', {})
    return render_template('play_wordle.html', game=game, wordle_game=wordle_game)

def extract_saved_word(pairs):
    return pairs.split(';')[0].strip().lower() 

def get_congrats_music():
    music_files = [
        'evicted.mp3',
        'protagonist.mp3',
        '4am.mp3',
        'princeton.mp3',
        'wave.mp3',
        'propeller.mp3',
        'eurostar.mp3',
        'coming.mp3',
        'letgo.mp3',
        'higher.mp3'
    ]
    return music_files

# serve music
@app.route('/music/<filename>')
def serve_music(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'music'), filename)

# validate word
@app.route('/api/validate_word', methods=['GET', 'POST'])
def validate_word():
    data = request.get_json()
    word = data.get('word', "").lower()
    if not word:
        return jsonify({'valid': False, 'message': 'No word was found.'}), 400

    api_key = app.config['MW_API_KEY'] 
    if not api_key:
        return jsonify({'valid': False, 'message': 'No API key.'}), 500

    response = requests.get(
        f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}",
        params={'key': api_key}
    )
    data = response.json()
    is_valid = bool(data and isinstance(data, list) and isinstance(data[0], dict))
    return jsonify({'valid': is_valid})

@app.route('/completed_games')
@login_required
def completed_games():
    user_games = UserGame.get_by_user(session['user_id'])
    return render_template('completed_games.html', user_games=user_games)

@app.route('/profile')
@login_required
def profile():
    user = User.get_by_id(session['user_id'])
    user_games = UserGame.get_by_user(session['user_id'])
    return render_template('profile', user=user, user_games=user_games)

# u can earn credits by winning games
@app.route('/credits')
@login_required
def credits():
    user_id = session['user_id']
    conn = Database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT games_played, won_first_attempt
        FROM statistics
        WHERE user_id = ? AND game_type = 'Wordle'
    ''', (user_id,))
    stats = cursor.fetchone()
    conn.close()
    
    if stats:
        credits = stats['games_played'] * 10 + stats['won_first_attempt'] * 50
    else:
        credits = 0

    return render_template('credits', credits=credits)

# play connections
@app.route('/play_connections/<int:game_id>', methods=['GET', 'POST'])
@login_required
def play_connections(game_id):
    game = Game.get_by_id(game_id)
    if not game:
        flash("Game not found!", "danger")
        return redirect(url_for('home'))
    
    user_id = session['user_id']

    # Initialize game state in session if not present
    if 'connections_game' not in session or session['connections_game']['game_id'] != game_id:
        session['connections_game'] = {
            'game_id': game_id,
            'completed_groups': CompletedGroup.get_completed_groups(user_id, game_id),
            'start_time': time.time()
        }

    if request.method == 'POST':
        data = request.get_json()
        selected_words = data.get('selected_words', [])

        if len(selected_words) != 4:
            return jsonify({'status': 'error', 'message': 'You must select exactly four words.'}), 400

        # Parse the groups from the game
        groups = game['pairs'].split(';')  # Assuming each group is separated by ';'
        parsed_groups = []
        for group in groups:
            parts = group.split(',')
            group_name = parts[0].strip()
            group_words = [word.strip().lower() for word in parts[1:]]
            parsed_groups.append({'name': group_name, 'words': group_words})

        # Check if the selected words match any group
        matched_group = None
        for grp in parsed_groups:
            if set(selected_words) == set(grp['words']) and grp['name'] not in session['connections_game']['completed_groups']:
                matched_group = grp
                break

        if matched_group:
            # Mark group as completed
            CompletedGroup.create(user_id, game_id, matched_group['name'])
            session['connections_game']['completed_groups'].append(matched_group['name'])

            # Update user statistics (e.g., credits)
            # For example, award 100 credits per completed group
            if 'credits' not in session:
                session['credits'] = 0
            session['credits'] += 100  # Adjust as needed

            return jsonify({'status': 'success', 'message': f"Found group: {matched_group['name']}"})
        else:
            return jsonify({'status': 'fail', 'message': "Incorrect selection. Try again."}), 400

    # On GET, render the play_connections.html template
    completed_groups = session['connections_game']['completed_groups']
    return render_template('play_connections.html', game=game, completed_groups=completed_groups)

# error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
