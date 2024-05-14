from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, send, emit
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Socket.IO
socketio = SocketIO(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    challenges = db.Column(db.String)

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    word = db.Column(db.String(250), nullable=False)
    hint = db.Column(db.String(250), nullable=False)
    player = db.Column(db.String(250), nullable=False)
    accepted = db.Column(db.Integer, default=0)
    seen = db.Column(db.Integer, default=0)
    seen_sender = db.Column(db.Integer, default=0)
    won = db.Column(db.Integer, default=0)
    sent_at = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime)

with app.app_context():
    db.create_all()

# # Function to create a connection to the SQLite database
# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# # Function to initialize the database
# def init_db():
#     conn = get_db_connection()
#     with app.open_resource('schema.sql', mode='r') as f:
#         conn.cursor().executescript(f.read())
#     conn.commit()
#     conn.close()

# # Initialize the database
# init_db()


# to get the challenges for users
def get_all_challenges():
    all_challanges = db.session.execute(db.select(Challenge).where(or_(Challenge.player == session['username'], Challenge.username == session['username'])).order_by(Challenge.id.desc())).scalars().all()
    return all_challanges

def get_all_unread_notifications():
    all_c = get_all_challenges()
    n = 0
    for c in all_c:
        if c.player == session['username'] and (not c.seen):
            n+=1
        elif c.username == session['username'] and c.accepted and (not c.seen_sender):
            n+=1
    return n

def newChallenge(word, hint, player):
    sent_at = datetime.now()
    new_c = Challenge(
        username = session['username'],
        word = word,
        hint = hint,
        player = player,
        sent_at = sent_at
    )
    db.session.add(new_c)
    db.session.commit()

# # Websocket for notifications - Just for connection purpose
# @socketio.on('my event')
# def handle_message(data):
#     print('received message: ' + data['data'])

# # Websocket for sending notification
# @socketio.on('message')
# def handle_message(message):
#     print(f'Received message: {message}')
#     send(message, broadcast=True)


# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error_msg="Passwords do not match. Please try again.")
        
        existing_user = db.session.execute(db.select(User).where(User.username == username)).scalar()
        
        if existing_user:
            return render_template('signup.html', error_msg="User already exists. Please choose a different username.")
        
        new_user = User(
            username = username,
            password = password,
        )
        db.session.add(new_user)
        db.session.commit()

        # Pass a success message to the template
        return render_template('signup.html', success_msg="Account has been created successfully!")

    return render_template('signup.html')




# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.session.execute(db.select(User).where(User.username == username, User.password==password)).scalar()

        if user:
            # Store the username in the session
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # Pass the error message to the template
            return render_template('login.html', msg="Invalid username or password. Please try again.")

    return render_template('login.html')


# Route for the home page
@app.route('/')
def home():
    # Check if username is stored in session, if not redirect to login
    if 'username' in session:
        username = session['username']
        all_c = get_all_challenges()

        return render_template('index.html', name=username, all_c=all_c, n_not=get_all_unread_notifications())
    else:
        return redirect(url_for('guest'))
    
@app.route('/guest')
def guest():
    # Check if username is stored in session, if not redirect to login
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('guest.html')

@app.route('/notification-seen')
def notificationSeen():
    c1 = get_all_challenges()
    for c in c1:
        if c.player == session['username']:
            c.seen = 1
        elif c.accepted and c.username == session['username']:
            c.seen_sender = 1
    db.session.commit()
    return ''

@app.route('/challenge-won/<id>')
def challenge_won(id):
    c1 = db.session.execute(db.select(Challenge).where(Challenge.id == id)).scalar()
    c1.won = 1
    db.session.commit()
    challenge_accepted(id)
    return ''

@app.route('/challenge-accepted/<id>')
def challenge_accepted(id):
    completed_at = datetime.now()
    c1 = db.session.execute(db.select(Challenge).where(Challenge.id == id)).scalar()
    c1.accepted = 1
    c1.completed_at = completed_at
    db.session.commit()
    return ''

@app.route('/accepted-challenge/<id>')
def a_challenge(id):
    completed_at = datetime.now()
    c1 = db.session.execute(db.select(Challenge).where(Challenge.id == id)).scalar()
    c1.accepted = 1
    c1.completed_at = completed_at
    db.session.commit()
    return ''


@app.route('/two-player-challenge', methods=["POST", "GET"])
def twoPlayerChallenge():
    error = None
    if request.method == 'POST':
        word = request.form.get('word')
        hint = request.form.get('hint')
        player = request.form.get('player')

        user_exists = db.session.execute(db.select(User).where(User.username==player)).scalar()
        if not user_exists:
            error = "Username doesn't exist, please try again."
        else:
            newChallenge(word, hint, player)
            flash("Challenge sent Successfully!")
            return redirect(url_for('home'))
        
    users = db.session.execute(db.select(User)).scalars()
    return render_template('new-challenge.html', name=session['username'], users=users, all_c=get_all_challenges(), n_not=get_all_unread_notifications(), error=error)


@app.route('/get-challenge/<id>')
def getChallenge(id):
    word = db.session.execute(db.select(Challenge).where(Challenge.id == id)).scalar()
    return word

def get_leaderboard_data():
    leaderboard_data = db.session.execute(db.select(User.username, User.score).order_by(User.score.desc()))
    return leaderboard_data

@app.route('/leader_board')
def leader_board():
    # Fetch leaderboard data
    leaderboard_data = get_leaderboard_data()
    
    # Check if username is stored in session, if not redirect to login
    if 'username' in session:
        username = session['username']
        return render_template('leader_board.html', users=leaderboard_data, name=username, all_c=get_all_challenges(), n_not=get_all_unread_notifications())
    else:
        return redirect(url_for('login'))
    

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/users')
def show_users():
    users = db.session.execute(db.select(User)).scalars()
    return render_template('users.html', users=users)


@app.route('/increment_score', methods=['POST'])
def increment_score():
    u1 = db.session.execute(db.select(User).where(User.username == session['username'])).scalar()
    data = request.json
    if data['difficulty'] == 'competitive':
        u1.score += 1
        db.session.commit()
    return 'Score updated'


@app.route('/decrement_score', methods=['POST'])
def decrement_score():
    u1 = db.session.execute(db.select(User).where(User.username == session['username'])).scalar()
    data = request.json
    if data['difficulty'] == 'competitive':
        u1.score -= 1
        db.session.commit()

    return 'Score updated'


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5005)
    # app.run(debug=True, port=5005)