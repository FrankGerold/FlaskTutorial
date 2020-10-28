from flask import Flask, g, render_template, request, session, flash, redirect, url_for
import sqlite3

# Config
DATABASE = "franker.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "change_me"

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


@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to db"""
    if not session.get('logged_in'):
        abort(401)

    db=get_db()
    db.execute(
        'insert into entries (title, text) values (?, ?)',
        [request.form['title'], request.form['text']]
    )
    db.commit()
    flash('New entry successfully posted!')
    return redirect(url_for('index'))

# root url
@app.route('/')
def index():
    """Searches DB for entries, then displays them"""
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


# make executable
if __name__ == '__main__':
    app.run()
