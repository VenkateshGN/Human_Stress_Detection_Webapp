from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from joblib import load  # For loading the ML model
import os
from datetime import timedelta
from emotion_analysis import analyze_emotions


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Route: Initialize Database
@app.route('/init_db')
def init_db():
    """Creates all necessary tables."""
    with app.app_context():
        db.create_all()
    return "Database initialized and tables created!"

# Route: Home
@app.route('/')
def home():
    username = session.get('username')
    return render_template('InterfaceIndex.html', username=username)

@app.route("/view_users")
def view_users():
    # Fetch all users using SQLAlchemy
    users = User.query.all()
    return render_template("view_users.html", users=users)

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session.permanent = True
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "error")
    return render_template('login.html')

# Route: Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different one.", "error")
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please use a different one.", "error")
            return render_template('register.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# Route: Logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' not in session:
        flash('You are not logged in!', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_username = request.form.get('username')  # Username entered by the user
        entered_password = request.form.get('password')  # Password entered by the user

        # Fetch user from the database based on the session's username
        user = User.query.filter_by(username=session['username']).first()

        if user and user.username == entered_username and check_password_hash(user.password, entered_password):
            # Username and password both verified; log the user out
            session.pop('username', None)
            flash('You have been logged out successfully.', 'success')
            return redirect(url_for('home'))
        else:
            # Either username or password is incorrect
            flash('Incorrect username or password. Please try again.', 'error')

    # Render the logout confirmation form
    return render_template('logout.html')


# Route: Take Test
@app.route('/take_test', methods=['GET', 'POST'])
def take_test():
    if 'username' not in session:
        flash('You must be logged in to take the test.', 'error')
        return redirect(url_for('login'))
    return render_template('take_test.html')
   


@app.route('/emotion_analysis')
def emotion_analysis():
    # Use imported analyze_emotions function
    chart_details = analyze_emotions()  # Get the emotion analysis details

    return render_template('result.html', 
                           emotion_counts=chart_details["counts"], 
                           line_chart_path=chart_details['line_chart_path'])  # Pass the chart details to the template


if __name__ == '__main__':
    app.run(debug=True)

