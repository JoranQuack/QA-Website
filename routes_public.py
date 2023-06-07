'''all frontend route functions'''
from datetime import datetime
from flask import Blueprint, render_template
from prisma.partials import AlbumWithMedia
from functions import get_about, get_people, get_events, get_albums, get_gallery, remove_old_events


api = Blueprint('', __name__)


@api.get('/')
def home_page():
    """navigates to home page after fetching its contents"""
    target = "get_home_contents"
    title = "Home"
    return render_template('loading.html', target=target, title=title)


@api.get('/album/<int:album_id>')
def album_page(album_id: int):
    """navigates to album page after fetching its contents"""
    target = f"get_album_contents/{album_id}"
    title = "Album"
    return render_template('loading.html', target=target, title=title)


@api.get('/get_home_contents')
def get_home():
    """gets home page contents"""
    remove_old_events()
    return render_template('home.html', datetime=datetime, albums=get_albums(True),
                           events=get_events(True), people=get_people(True),
                           gallery_cover=get_gallery(), about=get_about())


@api.get('/album/get_album_contents/<int:album_id>')
def get_album(album_id: int):
    """gets album contents"""
    album = AlbumWithMedia.prisma().find_first(
        where={'id': album_id}, include={'media': True})
    assert album is not None
    media = album.media
    has_media = len(media) > 0
    return render_template('album.html', media=media, album=album, has_media=has_media)


@api.get('/robots.txt')
def robots():
    """let robots access the .txt"""
    with open(file='robots.txt', encoding='utf-8', mode="r") as file:
        contents = file.read()
        file.close()
    return contents
