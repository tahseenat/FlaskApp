from flask import Flask, redirect, url_for, request
from flask import Flask, render_template
import jwt
from datetime import datetime, timedelta
import json
from aiohttp import web

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

app = Flask(__name__)


@app.route('/success')
def success(token):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args.get('username')
        password = request.args.get('password')

    # return render_template('hello.html')
    return "hello"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args.get('username')
        password = request.args.get('password')

    payload = {
        'username': username,
        'password': password
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    # return redirect(url_for('success', token=jwt_token))
    return  redirect(url_for('success'))


if __name__ == '__main__':
    app.run(debug=True)
