from flask import Flask, redirect, url_for, request
from flask import Flask, render_template
import jwt
from datetime import datetime, timedelta
import json
from aiohttp import web

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

app = Flask(__name__)


@app.route('/success', methods=['POST', 'GET'])
def success():
    render_template('hello.html')
    if request.method == 'POST':
        image_url = request.form['image_url']
    else:
        image_url = request.args.get('image_url')
    # return redirect('success')
    # return render_template('hello.html')
    return "image_url"


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
    return redirect(url_for('success'))


if __name__ == '__main__':
    app.run(debug=True)
