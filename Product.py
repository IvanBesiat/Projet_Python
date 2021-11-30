from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('loginView.html')

@app.route('/view')
def display(name=None):
    return render_template('displayView.html', name=name)

