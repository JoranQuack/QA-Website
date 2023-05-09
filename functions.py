"""all functions needed in the routes (mostly for backend)"""
import hashlib
from typing import Any
from flask import session
from prisma.errors import ForeignKeyViolationError
from database import db
from environments import SALT


assert SALT is not None


def get_session_data(key: str) -> Any | None:
    '''Gets current userid from session'''
    return session.get(key)  # type: ignore


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
    """remove all users specified"""
    error = False
    try:
        for user_id in user_ids:
            db.user.delete(where={
                'id': user_id
            })
    except ForeignKeyViolationError:
        error = True
    return error


def create_user(username: str, password: str):
    """creates a new user"""
    db.user.create(data={
        'username': username,
        'password': password,
        'is_admin': False
    })


def find_user_entries(user_id: int):
    """finds out how many entries"""
    num_entries = 0

    num_entries += len(db.event.find_many(where={'user_id': user_id}))
    num_entries += len(db.about.find_many(where={'user_id': user_id}))
    num_entries += len(db.people.find_many(where={'user_id': user_id}))
    num_entries += len(db.album.find_many(where={'user_id': user_id}))
    num_entries += len(db.media.find_many(where={'user_id': user_id}))

    return num_entries