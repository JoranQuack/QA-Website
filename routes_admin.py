'''all backend routes'''
from typing import List
from flask import (
    Blueprint, request, session, render_template, redirect, url_for, flash
)
from functions import (
    signed_in, secure_password, strings_to_ints, toggle_admins, remove_users, create_user,
    find_user_entries
)
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
    user_entries: List[int] = []
    for user in users:
        entries = find_user_entries(user.id)
        user_entries.append(entries)
    return render_template('users.html', users=users, entries=user_entries, enumerate=enumerate)


@api.post('/update_users')
def update_users():
    """admins users and removes users"""
    admin_ids = strings_to_ints(request.form.getlist('admin_users'))
    remove_ids = strings_to_ints(request.form.getlist('remove_users'))

    if session['user'] not in admin_ids:
        flash("One may not dethrone oneself")
        return redirect(url_for('admin.users_page'))
    elif session['user'] in remove_ids:
        flash("One may not remove oneself")
        return redirect(url_for('admin.users_page'))

    toggle_admins(admin_ids)
    error = remove_users(remove_ids)
    if error:
        flash("A user has entries in the DB and cannot be removed")
        return redirect(url_for('admin.users_page'))

    flash("Updated users successfully!")
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
        flash("Wrong username or password")
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

    create_user(username, password)
    flash("Account created!")
    return redirect(url_for('admin.edit_page'))


@api.get('/logout')
def logout():
    """logs out the user"""
    session.clear()
    flash("User has logged out!")
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
