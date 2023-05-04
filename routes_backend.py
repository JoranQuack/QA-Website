'''all backend routes'''
from flask import Blueprint, render_template, redirect, url_for, request, flash
from functions import signed_in, secure_password
# from prisma.partials import AlbumWithCover, AlbumWithMedia
# from datetime import datetime
from database import db

api = Blueprint('api', __name__)


@api.get('/edit')
def edit_page():
    """renders the edit page, redirects if not signed in"""
    if signed_in():
        return render_template('edit.html')
    else:
        return redirect(url_for('api.signin_page'))


@api.get('/signin')
def signin_page():
    """renders the signin page"""
    return render_template('signin.html')


@api.post('/signin')
def signin():
    """signs in the user"""
    username = request.form['username']
    password = secure_password(request.form['password'])

    db_user = db.user.find_first(where={
        'username': username
    })

    if db_user is None or db_user.password != password:
        flash("Username or password is wrong")
        return redirect(url_for('api.signin_page'))
    else:
        return redirect(url_for('api.edit_page'))


@api.get('/create')
def create():
    """create temp database entries"""
    # db.event.create(data={
    #     "title": "Mayo Bday",
    #     "has_time": False,
    #     "description": "banana",
    #     "reference": "www.google.com",
    #     "user_id": 1,
    #     "location": "tinos' house",
    #     "scheduled": datetime(2006, 3, 1, 19, 00),
    # })

    # image_names = ["front.JPG", "front2.jfif", "front4.jpg", "front3.jpg", "front5.jpg",
    #                "front6.jpg", "front7.jpg", "front8.jpg", "front9.jpg",
    #                "front10.png", "front11.png"]

    # created_media = [db.media.create(data={
    #     "user_id": 1,
    #     "type": "image",
    #     "reference": image_name,
    #     "on_gallery": False,
    # }) for image_name in image_names]

    album_contents = db.album.create(data={
        "title": "LETS GO WOOOOOO",
        "user_id": 1,
        "description": "mayonaise everywhere",
        "cover_id": 49,
    })

    print('album contents', album_contents)

    # for image in created_media:
    #     db.media.update(data={
    #         "albums": {
    #             "connect": [{
    #                 "id": album_contents.id
    #             }]
    #         }
    #     }, where={
    #         "id": image.id,
    #     })
    #     print(album_contents.id)

    return redirect(url_for('home'))
