# pylint: disable=import-error
"""all route functions"""
from flask import Blueprint, render_template, redirect, url_for
# from environments import
# from database import database
# from environments import SALT
# import hashlib


api = Blueprint("", "routes")


@api.get('/')
def main():
    """catches request to redirect to homepage"""
    return render_template('loading.html')


@api.get('/gethomecontents')
def home():
    """home page with information sections"""
    # users = database.user.find_first(where={
    #     'password': 'piss',
    # })
    return render_template('index.html')


@api.get('/create')
def create():
    """create temp database entries"""
    return redirect(url_for('main'))


@api.get('/robots.txt')
def robots():
    """let robots access the .txt"""
    with open("robots.txt", encoding="utf-8") as file:
        contents = file.read()
    return contents
