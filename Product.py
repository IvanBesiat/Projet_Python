from flask import (Blueprint, Flask, g, redirect, render_template, request, session, url_for, flash, current_app)
import sqlite3
from flask.cli import with_appcontext
import click
import functools

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
bp = Blueprint('auth', __name__, url_prefix='auth')



app = Flask(__name__)

# Creating connection with SQLite db
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            "Product.db",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# add Python functions that will run these SQL commands
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# closed after the work is finished
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# call that function
app.teardown_appcontext(close_db)
# adds a new command that can be called with the flask command
app.cli.add_command(init_db_command)
    
@app.route('/login', methods=['GET', 'POST'] )
def login():
    error = None
    if request.method == 'POST':
        email =  request.form['email']
        password = generate_password_hash(request.form['password'])
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
@app.route('/login')
def logout():
    """deconnection and clear session"""
    session.clear()
    return render_template('login.html')

@app.route('/Products')
def display():
    return render_template('Products.html')

@app.route('/Product/<name>')
def display(name=None):
    return render_template('Product.html', name=name)
