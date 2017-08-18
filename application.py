import os
import re
from flask import Flask, jsonify, render_template, request, url_for, session, flash, redirect
from flask_session import Session
from flask_jsglue import JSGlue
from tempfile import mkdtemp
from passlib.apps import custom_app_context as pwd_context

from cs50 import SQL
from helpers import login_required

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

@app.route("/")
def index():
    """Home Page."""
    session.clear()
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register."""
    session.clear()
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    password = pwd_context.hash(request.form.get("password"))
    
    result = db.execute("INSERT INTO users (username, password) VALUES(:username, :password)", username=username, password=password)
    if not result:
        flash("username already exists.")
        return render_template("register.html")
    
    session["username"] = username
    flash("You have successfully registerd!")
    return redirect(url_for("logged"))


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    search = db.execute("SELECT * FROM users WHERE username = :username", username = username)
    if len(search) != 1 or not pwd_context.verify(password, search[0]["password"]):
        flash("Invalid username or password")
        return render_template("login.html")
    
    session["username"] = search[0]["username"]
    return redirect(url_for("logged"))

@app.route("/logged")
@login_required
def logged():
    """The home page after logging in """
    
    return render_template("logged.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/save", methods=["POST", "GET"])
def save():
    title = request.args.get("title")
    body = request.args.get("text")
    layer = request.args.get("layer")
    card_id = request.args.get("id")
    case = request.args.get("save_case")
    # 1 is a string not int (request.args.get("save_case") return a string)
    
    if case == '1':
        db.execute("INSERT INTO data (username, title, text, layer, id) VALUES(:username, :title, :body, :layer, :id)",
        username = session["username"], title=title, body=body, layer=layer, id=card_id)
        
    elif case == '2':
        db.execute("UPDATE data SET layer=:layer WHERE username=:username AND id=:id",
        layer=layer, username=session["username"], id=card_id)
        
    elif case == '3':
        db.execute("UPDATE data SET title=:title, text=:body WHERE username=:username AND id=:id",
        title=title, body=body, username=session["username"], id=card_id)
        
    else:
        db.execute("DELETE FROM data WHERE username=:username AND id=:id",
        username=session["username"], id=card_id)
        
    
    return ''

@app.route("/load")
def load():
    result = db.execute("SELECT title, text, layer, id FROM data WHERE username=:username", username=session['username'])
    result2 = []
    for row in result:
        result3 = {
            "title": row["title"],
            "text": row["text"],
            "layer": row["layer"],
            "id": row["id"]
        }
        result2.append(result3)
    return jsonify(result2)