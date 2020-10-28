from flask import Flask, g
import sqlite3

# Config
DATABASE = "flaskr.db"

# Create and initialize new flask app
app = Flask(__name__)

# load config
app.config.from_object(__name__)

# Connect to DB
def connect_db():
    """Connects to the database"""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

# Create the DB
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

# Open DB cxn
def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Close db cxn
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

# root url
@app.route('/')
def index():
    """Searches DB for entries, then displays them"""
    return 'Hello, World!'

# make executable
if __name__ == '__main__':
    app.run()
