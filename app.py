from flask import Flask, render_template, g, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

import os, hashlib

import models


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/qa.db'
app.secret_key = os.getenv('SECRETKEY')
db = SQLAlchemy(app)


SALT = os.getenv('SALT')
UPLOAD_FOLDER = 'static/images/'


@app.route('/')
def check():
    s = models.User.query.all()
    return redirect(url_for('home', users = s))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)