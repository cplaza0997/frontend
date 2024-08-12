from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash)
import os
import requests


app = Flask(__name__)
app.secret_key = os.urandom(24)


ENDPOINT_ROOT = os.getenv("ENDPOINT_ROOT")


@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('items'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    response = requests.post(f'{ENDPOINT_ROOT}/login',
                             json={"user": username, "password": password})
    if (response.status_code == 200 and
            response.json()['status'] == 'Authorized'):
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('items'))
    else:
        flash("Unauthorized access. Please try again.")
        return redirect(url_for('home'))


@app.route('/items')
def items():
    if 'logged_in' not in session:
        return render_template('unauthorized.html')
    response = requests.get(f'{ENDPOINT_ROOT}/items')
    print(response.content)
    return render_template('items.html', items=response.json()['items'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/health')
def health():
    return "OK", 200
