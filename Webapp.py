from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Session configuration (session expires after 30 minutes of inactivity)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database route
@app.route('/init_db')
def init_db():
    # This will create all the necessary tables
    with app.app_context():
        db.create_all()
    return "Database initialized and tables created!"

# Home route
@app.route('/')
def home():
    username = session.get('username')
    return render_template('InterfaceIndex.html', username=username)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session.permanent = True  # Make the session permanent (enabling session timeout)
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "error")
    
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Validate inputs
        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template('register.html')
        
        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return render_template('register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already exists. Please use a different one.", "error")
            return render_template('register.html')
        
        # Hash the password before saving
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        
        # Save the new user to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        # Check if the user is logged in and prompt for confirmation
        if 'username' in session:
            entered_password = request.form['password']
            user = User.query.filter_by(username=session.get('username')).first()

            # Verify the entered password
            if user and check_password_hash(user.password, entered_password):
                session.pop('username', None)  # Clear the session
                flash('You have been logged out successfully.', 'success')
                return redirect(url_for('home'))  # Redirect to home page after logout
            else:
                flash('Incorrect password. Please try again.', 'error')
                return render_template('logout.html')  # Stay on logout page to retry
        else:
            flash('You are not logged in!', 'error')
            return redirect(url_for('home'))  # Redirect to home if not logged in

    return render_template('logout.html')  # For GET request, show logout confirmation form

# Take test route
@app.route('/take_test')
def take_test():
    username = session.get('username')
    if not username:
        flash('You must be logged in to take the test.', 'error')
        return redirect(url_for('login'))
    return render_template('take_test.html')

# View all users route
@app.route('/view_users')
def view_users():
    # Fetch all users from the database
    users = User.query.all()
    # Return the usernames and emails in a simple HTML format
    return render_template('view_users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
