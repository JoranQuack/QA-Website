"""all functions needed in the routes (mostly for backend)"""
import os
import hashlib
import secrets
from datetime import datetime
from flask import session, flash
from prisma.errors import ForeignKeyViolationError
from prisma.partials import AlbumWithMedia, MediaWithAlbums
from database import db
from environments import SALT
from constants import UPLOAD_FOLDER, UPLOAD_EXTENSIONS


assert SALT is not None


def session_get(key: str) -> str:
    """returns the session result from the given key"""
    return session.get(key)  # type: ignore


def session_remove(key: str):
    """removes a session variable"""
    if key in session:
        session.pop(key)  # type: ignore


def signed_in():
    """checks if theres is a user in the session"""
    return 'user' in session


def secure_password(password: str):
    """hashes and salts the password for protection"""
    return hashlib.sha512((password + SALT).encode('utf-8')).hexdigest()


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
    return db.about.find_first()


def get_people(is_public: bool):
    """finds all people from the people table"""
    if is_public:
        return db.people.find_many(where={'is_active': True})
    return db.people.find_many()


def get_events(is_public: bool):
    """finds all events from the event table"""
    if is_public:
        return db.event.find_many(where={'is_active': True}, order={'scheduled': 'asc'})
    return db.event.find_many()


def get_albums(is_public: bool):
    """finds all the albums from the album table"""
    if is_public:
        return AlbumWithMedia.prisma().find_many(include={'media': True}, where={'is_active': True})
    return AlbumWithMedia.prisma().find_many(include={'media': True})


def get_media():
    """finds all the media from the media table"""
    return db.media.find_many()


def get_gallery():
    """gets the gallery image for the homepage"""
    return db.media.find_first(where={'on_gallery': True})


def get_file_path(file: str):
    """makes the path for the given file"""
    return os.path.join(UPLOAD_FOLDER, file)


def iso_to_datetime(iso_datetime: str):
    """returns a datetime object of the iso_datetime"""
    date, times = iso_datetime.split('T')
    year, month, day = date.split('-')
    hour, minute = times.split(':')

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
            session_remove('_flashes')
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


def get_used_media():
    """get all media that is being used in any album"""
    albums = AlbumWithMedia.prisma().find_many(include={'media': True})
    used_media: list[int] = []
    for album in albums:
        used_media += [album.media[i].id for i in range(len(album.media))]
    return used_media


def find_used_albums(media_id: int):
    """finds all used albums associated with a specific media"""
    used_albums = AlbumWithMedia.prisma().find_many(include={'media': True}, where={
        'media': {
            'some': {
                'id': media_id
            }
        }
    })
    return used_albums


def can_delete_media(used_albums: list[AlbumWithMedia]):
    """returns whether or not the media can be deleted"""
    return all(len(album.media) >= 3 for album in used_albums)


def disconnect_and_delete_media(media_id: int, used_albums: list[AlbumWithMedia]):
    """removes a media from existance in the database and all its foreign relationships"""

    for album in used_albums:
        db.album.update(where={'id': album.id}, data={
            'media': {
                'disconnect': [{'id': media_id}]
            }
        })
    db.media.delete(where={'id': media_id})


def replace_gallery_media(media_id: int):
    """replaces the current gallery media on the gallery with a new one"""

    db.media.update_many(where={'on_gallery': True}, data={
        'on_gallery': False})

    db.media.update(where={'id': media_id}, data={'on_gallery': True})


def is_on_gallery(media_id: int):
    """checks if a media is on gallery"""

    media = db.media.find_first(
        where={'id': media_id})

    assert media is not None

    return media.on_gallery


def remove_media(remove_media_ids: list[int]):
    """removes list of media"""
    used_media = get_used_media()

    message = "Deleted all media selected!"

    for media_id in remove_media_ids:

        if media_id in used_media:
            used_albums = find_used_albums(media_id)

            if can_delete_media(used_albums):
                disconnect_and_delete_media(media_id, used_albums)
            else:
                message = "Couldn't delete all media"

        elif is_on_gallery(media_id):
            message = "A media is used in the gallery"

        else:
            db.media.delete(where={'id': media_id})

    flash(message)


def random_filename(name: str):
    """makes a random filename"""
    extension = name.split('.')[-1]

    if extension.lower() not in UPLOAD_EXTENSIONS:
        raise ValueError('Invalid file extension')

    filename = secrets.token_bytes(32).hex()

    return f"{filename}.{extension}"


def image_clean():
    """removes unused images"""
    used_images: list[str] = []
    used_images += [media.reference for media in get_media()]
    used_images += [person.reference for person in get_people(False)]

    images = os.listdir(UPLOAD_FOLDER)

    for image in images:
        if image not in used_images and 'default' not in image:
            os.remove(f"{UPLOAD_FOLDER}/{image}")
