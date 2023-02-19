from flask import Flask, render_template, g, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker
from entities import *
import base
import os


app = Flask(__name__, template_folder="templates")
engine = create_engine('sqlite:///database/qa.db', echo = True)
session = sessionmaker(bind=engine)()
base.Base.metadata.create_all(engine)


@app.route('/')
def home():
    s = session.query(User).all()
    return render_template('home.html', users = s)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)