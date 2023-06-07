'''all backend routes'''
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, request, session, render_template, redirect, url_for, flash
)
from functions import (
    signed_in, secure_password, strings_to_ints, toggle_admins, remove_users, create_user,
    session_get, get_users, get_about, get_people, get_events, get_albums, get_media,
    get_file_path, iso_to_datetime, remove_old_events, find_unused_media, replace_gallery_media,
    remove_media, random_filename
)
from prisma.partials import AlbumWithMedia
from database import db

api = Blueprint('admin', __name__)


@api.get('/')
def edit_page():
    """renders the edit page, redirects if not signed in"""
    if not signed_in():
        return redirect(url_for('admin.signin_page'))
    remove_old_events()
    return render_template('edit.html', users=get_users(), about=get_about(), people=get_people(False),
                           events=get_events(False), albums=get_albums(False), media=get_media())


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
    image_upload = secure_filename(file.filename)  # type: ignore

    if image_upload != '':
        image_name = random_filename(image_upload)
        db.people.update(where={'id': person_id}, data={
            'reference': image_name
        })
        image_path = get_file_path(image_name)
        file.save(image_path)  # type: ignore

    has_filled = name != '' and role != ''
    styled_name = f" {name}".rstrip()

    if to_remove:
        db.people.delete(where={'id': person_id})
        flash(f"Removed{styled_name}!")
    elif has_filled:
        db.people.update(where={'id': person_id}, data={
            'name': name,
            'role': role,
            'is_active': is_active
        })
        flash(f"Updated{styled_name}!")
    else:
        flash("Name and role are required")
    return redirect(url_for('admin.edit_page'))


@api.get('/create_person')
def create_person():
    """makes a new person in the people table"""
    db.people.create(data={
        'user_id': session['user'],
        'name': '',
        'role': ''
    })
    flash("New person created!")
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
    to_remove = len(request.form.getlist('to_remove')) == 1

    has_filled = title != '' and description != '' and location != ''
    styled_title = f" {title}".rstrip()

    if to_remove:
        db.event.delete(where={'id': event_id})
        message = f"Removed{styled_title}!"

    elif has_filled:
        db.event.update(where={'id': event_id}, data={
            'title': title,
            'description': description,
            'location': location,
            'reference': reference,
            'scheduled': scheduled,
            'has_time': has_time,
            'is_active': is_active
        })
        message = f"Updated{styled_title}!"

    else:
        message = "Title, location, and description are required"

    flash(message)
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
    flash("New event created!")
    return redirect(url_for('admin.edit_page'))


@api.get('/edit_album/<int:album_id>')
def edit_album_page(album_id: int):
    """displays the inside of an album in a form to allow update"""

    album = AlbumWithMedia.prisma().find_first(
        where={'id': album_id}, include={'media': True})
    unused_media = find_unused_media(album_id)

    return render_template('edit_album.html', album=album, unused_media=unused_media,
                           is_forward=True)


@api.post('/create_album')
def create_album():
    """creates a new album"""
    db.album.create(data={
        'user_id': session['user'],
        'description': '',
        'title': ''
    })
    return redirect(url_for('admin.edit_page'))


@api.post('/update_album/<int:album_id>')
def update_album(album_id: int):
    """updates an album in the album table"""
    is_active = len(request.form.getlist('is_active')) == 1
    title = request.form['title']
    description = request.form['description']
    selected_media = strings_to_ints(request.form.getlist('selected_media'))

    if len(selected_media) < 2:
        flash("Select at least 2 media for one album")
    elif title == '' or description == '':
        flash("Title and description are required")
    else:
        db.album.update(where={'id': album_id}, data={
            'title': title,
            'description': description,
            'is_active': is_active,
            'media': {
                'set': [{'id': media_id} for media_id in selected_media],
            }
        })
        flash("Updated album!")

    return redirect(url_for('admin.edit_album_page', album_id=album_id))


@api.post('/remove_album/<int:album_id>')
def remove_album(album_id: int):
    """removes and album"""
    db.album.delete(where={'id': album_id})
    return redirect(url_for('admin.edit_page'))


@api.post('/create_media')
def create_media():
    """adds new media to db and uploads the image"""
    file = request.files['upload_media']
    image_upload = secure_filename(file.filename)  # type: ignore

    if image_upload != '':
        image_name = random_filename(image_upload)
        db.media.create(data={
            'user_id': session['user'],
            'reference': image_name,
            'type': 'image'
        })

        image_path = get_file_path(image_name)
        file.save(image_path)  # type: ignore
        message = "Added media!"

    else:
        message = "No file uploaded"

    flash(message)
    return redirect(url_for('admin.edit_page'))


@api.post('/update_media')
def update_media():
    """remove or update a media to be gallery"""
    is_removing = request.form['remove_or_update'] == "Remove all selected"
    selected_media = strings_to_ints(request.form.getlist('selected_media'))

    if is_removing:
        remove_media(selected_media)
    elif len(selected_media) == 1:
        replace_gallery_media(int(selected_media[0]))
        flash("Replaced gallery image!")
    else:
        flash("Only select 1 media to set as gallery image")

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
