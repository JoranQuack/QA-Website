# pylint: disable=import-error
"""all route functions"""
from flask import Blueprint, render_template
from environments import MAP_API_KEY
# from database import database
# from environments import SALT
# import hashlib


api = Blueprint("", "routes")


@api.get('/')
def check():
    """catches request to redirect to homepage"""
    return render_template('loading.html')


@api.get('/home')
def home():
    """home page with information sections"""
    # users = database.user.find_first(where={
    #     'password': 'piss',
    # })
    return render_template('home.html', map_api_key=MAP_API_KEY)
