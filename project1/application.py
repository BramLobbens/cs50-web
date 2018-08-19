import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Goodreads API
api_key = os.getenv("APP_API_KEY")

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL_P1"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL_P1"))
db = scoped_session(sessionmaker(bind=engine))

# TO DO: implement usage
# check project tips to use flask_session
# LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def index():
    """Main page"""
    
    return render_template("index.html")

#  Log-in and Registration Routes
@app.route("/registration")
def registration():
    """Registration page"""
    
    return render_template("registration.html")
    
@app.route("/register", methods=["POST"])
def register():
    """Register a user"""

    user_name = request.form.get("user_name")
    password = request.form.get("password")

    # Check if username exists
    if db.execute("SELECT id FROM users WHERE user_name = :user_name",
                  {"user_name": user_name}).rowcount != 0:
        return render_template("error.html", message="Username already exists.")

    # Insert user in database
    db.execute("INSERT INTO users (user_name, password) VALUES (:user_name, :password)",
               {"user_name": user_name, "password": password})

    db.commit()
    return render_template("success.html")

@app.route("/login", methods=["POST"])
#@login_manager.user_loader
def login():
    """Log in a user"""

    # TO DO: implement better and safer solution!
    global user_name
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    
    if db.execute("SELECT password FROM users WHERE user_name = :user_name",
                               {"user_name": user_name}).fetchone()[0] == password:
        return render_template("search.html", name=user_name)

    return render_template("error.html", message="Incorrect username or password.")

# Content Routes
@app.route("/find_book", methods=["POST"])
#@login_required
def find_book():
    """Search for books"""
    
    # logged in users can search for books
    query = request.form.get("search")
    res = db.execute("SELECT * FROM books WHERE author = :query",
                     {"query": query}).fetchall()
    return render_template("search.html", result=res, name=user_name)


    #res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": "9781632168146"})
    #foo = res.json()
