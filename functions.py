"""all functions needed in the routes (mostly for backend)"""
import hashlib
from typing import Any
from flask import session
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
    # type: ignore
    return hashlib.sha512(salted_password.encode('utf-8')).hexdigest()
