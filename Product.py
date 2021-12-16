from flask import Flask, render_template, url_for, request
import sqlite3
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
    
@app.route('/')
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['email'],
                       request.form['password']):
            return log_the_user_in(request.form['email'])
        else:
            error = 'invalid email/password'
    return render_template('login.html', error=error)

@app.route('/Products')
def display():
    return render_template('Products.html')

@app.route('/Product/<name>')
def display(name=None):
    return render_template('Product.html', name=name)
