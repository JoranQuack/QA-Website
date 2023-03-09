from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from database import db_session
from entities import *


api = Blueprint("", "routes")


@api.get('/')
def check():
    return redirect(url_for('home'))


@api.get('/home')
def home():
    s = db_session.query(User.username).one()
    return render_template('home.html', users = s)