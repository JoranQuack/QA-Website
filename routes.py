# pylint: disable=import-error
"""all route functions"""
from flask import Blueprint, render_template, redirect, url_for
from environments import MAP_API_KEY
from database import database
# from environments import SALT
# import hashlib


api = Blueprint("", "routes")


@api.get('/')
def check():
    """catches request to redirect to homepage"""
    return redirect(url_for('home'))


@api.get('/home')
def home():
    """home page with information sections"""
    users = database.user.find_first(where={
        'password': 'piss',
    })
    map_api_key = MAP_API_KEY
    return render_template('home.html', users=users, map_api_key=map_api_key)
