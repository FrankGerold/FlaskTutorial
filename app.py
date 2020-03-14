from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import sqlite3

# Configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'ayyy_lmao'
USERNAME = '123'
PASSWORD = '123'

# Create and Initialize app
app = Flask(__name__)
app.config.from_object(__name__)
#
# @app.route('/')
# def hello():
#     return 'Hello, World!'

# Connect to database
def connect_db():
    """
    Connects to database.
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# Create DB
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Open db connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Close db cnxn
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()













if __name__ == '__main__':
    init_db()
    app.run()
