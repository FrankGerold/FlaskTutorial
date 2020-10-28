from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify, abort
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

basedir = Path(__file__).resolve().parent

# Config
DATABASE = "frankr.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "change_me"
SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Create and initialize new flask app
app = Flask(__name__)

# load config
app.config.from_object(__name__)

# init sqlalchemy
db = SQLAlchemy(app)

# Models needs db to already exist, so import goes here!
from project import models

# # Connect to DB
# def connect_db():
#     """Connects to the database"""
#     rv = sqlite3.connect(app.config["DATABASE"])
#     rv.row_factory = sqlite3.Row
#     return rv
#

# # Create the DB
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource("schema.sql", mode="r") as f:
#             db.cursor().executescript(f.read())
#         db.commit()
#
#
# # Open DB cxn
# def get_db():
#     if not hasattr(g, "sqlite_db"):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# # Close db cxn
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, "sqlite_db"):
#         g.sqlite_db.close()
#

# Log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login, authentication, session management."""
    error = None

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


# Log out
@app.route('/logout')
def logout():
    """User logout, auth, session management"""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


# add post
@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to db"""
    if not session.get('logged_in'):
        abort(401)

    new_entry = models.Post(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()

    flash('New entry successfully posted!')
    return redirect(url_for('index'))


# Delete post
@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Delete post from db"""
    result = {'status': 0, 'message': 'Error'}
    try:
        db.session.query(models.Post).filter_by(id=post_id).delete()
        db.session.commit()

        result = {'status': 1, 'message': 'Post Deleted!'}
        flash('Entry Deleted')

    except Exception as e:
        result = {'status': 0, 'message': repr(e)}

    return jsonify(result)


# search
@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get('query')
    entries = db.session.query(models.Post)

    if query:
        return render_template('search.html', entries=entries, query=query)

    return render_template('search.html')


# root url
@app.route('/')
def index():
    """Searches DB for entries, then displays them"""
    entries = db.session.query(models.Post)
    return render_template('index.html', entries=entries)


# make executable
if __name__ == '__main__':
    app.run()
