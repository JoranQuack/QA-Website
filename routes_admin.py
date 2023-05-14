'''all backend routes'''
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, request, session, render_template, redirect, url_for, flash
)
from functions import (
    signed_in, secure_password, strings_to_ints, toggle_admins, remove_users, create_user,
    session_get, get_users, get_about, get_people, get_events, get_file_path, iso_to_datetime,
    remove_old_events
)
from database import db

api = Blueprint('admin', __name__)


@api.get('/')
def edit_page():
    """renders the edit page, redirects if not signed in"""
    if not signed_in():
        return redirect(url_for('admin.signin_page'))
    remove_old_events()
    return render_template('edit.html', users=get_users(), about=get_about(), people=get_people(),
                           events=get_events())


@api.post('/update_users')
def update_users():
    """admins users and removes users"""
    admin_ids = strings_to_ints(request.form.getlist('admin_users'))
    remove_ids = strings_to_ints(request.form.getlist('remove_users'))

    message = "Updated users successfully!"
    if session['user'] not in admin_ids:
        message = "One may not dethrone oneself"
    elif session['user'] in remove_ids:
        message = "One may not remove oneself"
    elif not remove_users(remove_ids):
        message = "Some accounts could not be removed"
    toggle_admins(admin_ids)

    flash(message)
    return redirect(url_for('admin.edit_page'))


@api.post('/update_about')
def update_about():
    """updates the about section"""
    word_min = 200
    word_max = 700

    new_description = request.form['description']
    user_id = int(session_get('user'))

    if word_min > len(new_description) > word_max:
        session['description'] = new_description
        flash(f"Please write between {word_min} and {word_max} characters")
        return redirect(url_for('admin.edit_page'))

    db.about.delete_many()
    db.about.create(data={
        'user_id': user_id,
        'description': new_description,
        'location': 'default'
    })

    flash("Updated about successfully!")
    return redirect(url_for('admin.edit_page'))


@api.post('/update_person/<int:person_id>')
def update_person(person_id: int):
    """updates one person in the people table"""
    name = request.form['name'].title()
    role = request.form['role'].title()
    is_active = len(request.form.getlist('is_active')) == 1
    to_remove = len(request.form.getlist('to_remove')) == 1
    file = request.files['image']
    image = secure_filename(file.filename)  # type: ignore

    db.people.update(where={'id': person_id}, data={
        'name': name,
        'role': role,
        'is_active': is_active
    })

    if image != '':
        db.people.update(where={'id': person_id}, data={
            'reference': image
        })
        image_path = get_file_path(image)
        file.save(image_path)  # type: ignore

    if to_remove:
        db.people.delete(where={'id': person_id})
    return redirect(url_for('admin.edit_page'))


@api.get('/create_person')
def create_person():
    """makes a new person in the people table"""
    db.people.create(data={
        'user_id': session['user'],
        'name': '',
        'role': ''
    })
    return redirect(url_for('admin.edit_page'))


@api.post('/update_event/<int:event_id>')
def update_event(event_id: int):
    """updates event specified by id"""
    title = request.form['title'].title()
    location = request.form['location'].title()
    description = request.form['description']
    reference = request.form['reference']
    scheduled = iso_to_datetime(request.form['scheduled'])
    has_time = len(request.form.getlist('has_time')) == 1
    is_active = len(request.form.getlist('is_active')) == 1

    db.event.update(where={'id':event_id}, data={
        'title': title,
        'description': description,
        'location': location,
        'reference': reference,
        'scheduled': scheduled,
        'has_time': has_time,
        'is_active': is_active
    })

    return redirect(url_for('admin.edit_page'))


@api.get('/create_event')
def create_event():
    """creates an event"""
    db.event.create(data={
        'user_id': session['user'],
        'title': '',
        'description': '',
        'has_time': True,
        'location': ''
    })
    return redirect(url_for('admin.edit_page'))


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
