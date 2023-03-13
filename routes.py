"""all route functions"""
from flask import Blueprint, render_template, redirect, url_for
from database import get_db


api = Blueprint("", "routes")


@api.get('/')
def check():
    """catches request to redirect to homepage"""
    return redirect(url_for('home'))


@api.get('/home')
def home():
    """home page with information sections"""
    users = get_db().user.find_first(where={
        'password': 'piss',
    })
    if users is not None:
        users.dict()
    return render_template('home.html', users=users)
