'''all backend routes'''
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functions import signed_in, secure_password
# from prisma.partials import AlbumWithCover, AlbumWithMedia
# from datetime import datetime
from database import db

api = Blueprint('admin', __name__)


@api.get('/')
def edit_page():
    """renders the edit page, redirects if not signed in"""
    if not signed_in():
        return redirect(url_for('admin.signin_page'))
    return render_template('edit.html')


@api.get('/users')
def users_page():
    """the page where admins can manage other users"""
    users = db.user.find_many()
    return render_template('users.html', users=users)


@api.post('/user_admin')
def user_admin():
    """makes users admins or not admins"""
    admins = request.form['is_admin']
    print(admins)
    return redirect(url_for('admin.users_page'))


@api.get('/signin')
def signin_page():
    """renders the signin page"""
    return render_template('signin.html', sign_page=True)


@api.post('/signin')
def signin():
    """signs in the user"""
    username = request.form['username']
    password = secure_password(request.form['password'])

    user = db.user.find_first(where={
        'username': username
    })

    if user is None or user.password != password:
        flash("Username or password is wrong")
        return redirect(url_for('admin.signin_page'))
    session['user'] = user.id
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    flash(f"Welcome, {username}!")
    return redirect(url_for('admin.edit_page'))


@api.get('/signup')
def signup_page():
    """renders the signup page"""
    return render_template('signup.html', sign_page=True)


@api.post('/signup')
def signup():
    """signs up a new user"""
    username = request.form['username'].lower()
    password = secure_password(request.form['password'])
    confirm_password = secure_password(request.form['confirm-password'])

    user = db.user.find_first(where={
        'username': username.lower()
    })

    if password != confirm_password:
        flash("Passwords don't match")
        return redirect(url_for('admin.signup'))
    elif user is not None:
        flash("Username is already taken")
        return redirect(url_for('admin.signup'))

    db.user.create(data={
        'username': username,
        'password': password,
        'is_admin': False
    })

    flash("Account created!")
    return redirect(url_for('admin.edit_page'))


@api.get('/logout')
def logout():
    """logs out the user"""
    session.clear()
    return redirect(url_for('admin.edit_page'))


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
