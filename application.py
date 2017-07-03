from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    stocks = db.execute("SELECT symbol, name, shares, price, TOTAL FROM portfolio WHERE id = :id", id = session["user_id"])
    for stock in stocks:
        stock["price"] = usd(stock["price"])
        stock["TOTAL"] = usd(stock["TOTAL"])

    row = db.execute("SELECT cash, stocks_value FROM users WHERE id = :id", id = session["user_id"])
    cash = usd(row[0]["cash"])
    stocks_value = row[0]["stocks_value"]
    try:
        return render_template("index.html", stocks=stocks, cash = cash, stocks_total = usd(stocks_value))
    except:
        return render_template("index.html", cash = cash, stocks_total = stocks_value)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL")

        if not request.form.get("shares"):
            return apology("PROVIDE NUMBER OF SHARES")

        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("INVALID SYMBOL")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("INVALID SHARES")
        
        total = shares * symbol["price"]
        row = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        
        if row[0]['cash'] < total:
            return apology("CAN'T AFFORD")
        
        symbol_db = db.execute("SELECT symbol FROM portfolio WHERE id = :id AND symbol = :symbol",
        id = session["user_id"], symbol = request.form.get("symbol").upper())
        try:
            if symbol_db[0]["symbol"] == request.form.get("symbol").upper():
                db.execute("UPDATE portfolio SET shares = shares + :shares, TOTAL = TOTAL + :TOTAL WHERE id = :id AND symbol = :symbol",
                shares = shares, TOTAL = total, id = session["user_id"], symbol = request.form.get("symbol").upper())
        
        except:
            db.execute("INSERT INTO portfolio (id, symbol, name, shares, price, TOTAL) VALUES(:id, :symbol, :name, :shares, :price, :TOTAL)",
            id = session["user_id"], symbol = symbol["symbol"], name = symbol["name"], shares = shares, price = symbol["price"], TOTAL = total)
        
        db.execute("UPDATE users SET cash = cash - :total, stocks_value = stocks_value + :total WHERE id = :id",
        id = session["user_id"], total = total)
        
        # for history
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :price)",
        id = session["user_id"], symbol = symbol["symbol"], shares = shares, price = symbol["price"])
        return redirect(url_for("index"))
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    stocks = db.execute("SELECT symbol, shares, price, TRANSACTED FROM history WHERE id = :id", id = session["user_id"])
    for stock in stocks:
        stock["price"] = usd(stock["price"])
    
    return render_template("history.html", stocks = stocks)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method =="POST":
        if not request.form.get("quote"):
            return apology("provide symbol")
        quote = lookup(request.form.get("quote"))
        if not quote:
            return apology("Invalid Symbol")
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price = usd(quote["price"]))
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("missing username")
        
        if not request.form.get("password"):
            return apology("must provide password")
        
        if not request.form.get("confirmation"):
            return apology("must confirm password")
        
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("password does not match")
        
        username = request.form.get("username")
        password = pwd_context.encrypt(request.form.get("password"))
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=password)
        if not result:
            return apology("username already exists")
        
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = username)
        if not rows:
            return apology("error")
        session["user_id"] = rows[0]["id"]
        return redirect(url_for("index"))
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL")
        
        if not request.form.get("shares"):
            return apology("PROVIDE NUMBER OF SHARES")
        
        # search for symbol and its information
        search = db.execute("SELECT * FROM portfolio WHERE id = :id AND symbol = :symbol",
        id = session["user_id"], symbol = request.form.get("symbol").upper())
        if not search:
            return apology("SHARES NOT OWNED")
        
        symbol = search[0]["symbol"].upper()    
        
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("INVALID SHARES")
        
        shares_db = search[0]["shares"]
        if shares > shares_db:
            return apology("TOO MANY SHARES")
        
        price = search[0]["price"]
        
        total = search[0]["TOTAL"] - shares * price
        sold = shares * price
        
        if shares == shares_db:
            db.execute("DELETE FROM portfolio WHERE id = :id AND symbol = :symbol", id = session["user_id"], symbol = symbol)
        else:
            db.execute("UPDATE portfolio SET shares = shares - :shares, TOTAL = :TOTAL WHERE id = :id AND symbol = :symbol",
            id = session["user_id"], shares = shares, TOTAL = total, symbol = symbol)
        
        db.execute("UPDATE users SET cash = cash + :TOTAL, stocks_value = stocks_value - :TOTAL WHERE id = :id",
        id = session["user_id"], TOTAL = sold)
        
        # for history
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :price)",
        id = session["user_id"], symbol = symbol, shares = -shares, price = price)
        
        return redirect(url_for("index"))
    else:
        return render_template("sell.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        if not request.form.get("curpassword"):
            return apology("provide your current password")
        
        if not request.form.get("newpassword"):
            return apology("provide new password")
        
        if not request.form.get("confirmation"):
            return apology("must confirm password")
        
        hash_db = db.execute("SELECT hash FROM users WHERE id = :id", id = session["user_id"])
        
        cur_hash = hash_db[0]["hash"]
        if not pwd_context.verify(request.form.get("curpassword"), cur_hash):
            return apology("CURRENT PASSWORD IS WRONG")
        
        if request.form.get("confirmation") != request.form.get("newpassword"):
            return apology("new password does not match")
        
        if request.form.get("curpassword") == request.form.get("newpassword"):
            return apology("current and new passwords are the same")
        
        newpassword = pwd_context.encrypt(request.form.get("newpassword"))
        db.execute("UPDATE users SET hash = :hash WHERE id = :id",
        hash = newpassword, id = session["user_id"])
        return render_template("login.html")
    else:
        return render_template("change.html")