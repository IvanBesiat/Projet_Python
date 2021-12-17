from typing import Counter
from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from werkzeug.security import check_password_hash
from flask import current_app, g
from flask.cli import with_appcontext
import click


app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            "Product.db",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

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

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    
# Function login for the application
@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    #  Login or Register.
    # Powered by Flask-Login.
    # Error message is sent to connection page in case of wrong password or
    # in case of already existing user.
    # 
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone() 
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('products'))

        flash(error)

    return render_template('login.html')

# call the function logout and close the session
def logout():
    """deconnection and clear session"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/Products', methods=('GET', 'POST'))
def products():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    print(products)
    return render_template('Products.html', products=products)

@app.route('/Product/<name>', methods=('GET', 'POST'))
def product(name=None):
    return render_template('Product.html', name=name)
