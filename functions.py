"""all functions needed in the routes (mostly for backend)"""
import os
import hashlib
from datetime import datetime
from flask import session, flash
from prisma.errors import ForeignKeyViolationError
from prisma.partials import AlbumWithCover, MediaWithAlbums
from database import db
from environments import SALT


assert SALT is not None

UPLOAD_FOLDER = 'static/images/uploaded'


def session_get(key: str) -> str:
    """returns the session result from the given key"""
    result: str = session.get(key)  # type: ignore
    return result


def session_remove(key: str):
    """removes a session variable"""
    session.pop(key)  # type: ignore


def signed_in():
    """checks if theres is a user in the session"""
    return 'user' in session


def secure_password(password: str):
    """hashes and salts the password for protection"""
    salted_password = password + SALT
    return hashlib.sha512(salted_password.encode('utf-8')).hexdigest()


def strings_to_ints(numbers: list[str]):
    """converts list of strings to list of ints"""
    return [int(number) for number in numbers]


def toggle_admins(admin_ids: list[int]):
    """set all specified users into admins and set all other users to non-admins"""
    users = db.user.find_many()
    user_ids = [user.id for user in users]

    for user_id in user_ids:
        is_admin = user_id in admin_ids
        db.user.update(where={
            'id': user_id
        }, data={
            'is_admin': is_admin
        })


def remove_users(user_ids: list[int]):
    """remove all users specified, return bool representing whether or not it was successful"""
    try:
        for user_id in user_ids:
            db.user.delete(where={
                'id': user_id
            })
    except ForeignKeyViolationError:
        return False
    return True


def create_user(username: str, password: str):
    """creates a new user"""
    db.user.create(data={
        'username': username,
        'password': password,
        'is_admin': False
    })


def find_user_entries(user_id: int):
    """finds out how many entries in the database a user has"""
    num_entries = 0

    num_entries += len(db.event.find_many(where={'user_id': user_id}))
    num_entries += len(db.about.find_many(where={'user_id': user_id}))
    num_entries += len(db.people.find_many(where={'user_id': user_id}))
    num_entries += len(db.album.find_many(where={'user_id': user_id}))
    num_entries += len(db.media.find_many(where={'user_id': user_id}))

    return num_entries


def get_users():
    """finds all required variables (+ entries) for a list of users"""
    users = db.user.find_many()
    entries: list[int] = []
    for user in users:
        entries.append(find_user_entries(user.id))
    return zip(users, entries)


def get_about():
    """finds the about section info"""
    about = db.about.find_first()
    assert about is not None
    return about


def get_people():
    """finds all people from the people table"""
    people = db.people.find_many()
    return people


def get_events():
    """finds all events from the event table"""
    events = db.event.find_many()
    return events


def get_albums():
    """finds all the albums from the album table"""
    albums = AlbumWithCover.prisma().find_many(include={'cover': True})
    return albums


def get_file_path(file: str):
    """makes the path for the given file"""
    path = os.path.join(UPLOAD_FOLDER, file)
    return path


def iso_to_datetime(iso_datetime: str):
    """returns a datetime object of the iso_datetime"""
    date, time = iso_datetime.split('T')
    year, month, day = date.split('-')
    hour, minute = time.split(':')
    datetime_object = datetime(int(year), int(
        month), int(day), int(hour), int(minute))
    return datetime_object


def remove_old_events():
    """removes events that have already passed that are stored in the database"""
    events = db.event.find_many()
    current_datetime = datetime.now().timestamp()
    for event in events:
        event_datetime = event.scheduled.timestamp()
        if event_datetime + 86400 < current_datetime:
            db.event.delete(where={'id': event.id})
            flash("Removed an old event")


def find_unused_media(album_id: int):
    """finds all the media from the media table that is not used in a specific album"""
    all_media = MediaWithAlbums.prisma().find_many(include={'albums': True})
    unused_media: list[MediaWithAlbums] = []
    for media in all_media:
        album_ids: list[int] = []
        for album in media.albums:
            album_ids.append(album.id)
        if album_id not in album_ids:
            unused_media.append(media)
    return unused_media
