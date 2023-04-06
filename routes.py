# pylint: disable=import-error
"""all route functions"""
# import time
from flask import Blueprint, render_template, redirect, url_for
# from environments import
# from database import database
# from environments import SALT
# import hashlib


api = Blueprint("", "routes")


@api.get('/')
def home():
    """navigates to home page after fetching its contents"""
    target = "get_home_contents"
    title = "Home"
    return render_template('loading.html', target=target, title=title)


@api.get('/album/<int:album_id>')
def album(album_id: int):
    """navigates to album page after fetching its contents"""
    target = f"get_album_contents/{album_id}"
    title = "Album"
    return render_template('loading.html', target=target, title=title)


@api.get('/get_home_contents')
def get_home():
    """gets home page contents"""
    # users = database.user.find_first(where={
    #     'password': 'piss',
    # })
    # time.sleep(5)
    return render_template('home.html')


@api.get('/album/get_album_contents/<int:album_id>')
def get_album(album_id: int):
    """gets album contents"""
    return render_template('album.html', album_id=album_id)


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
