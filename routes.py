'''all route functions'''
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
# from environments import
from database import db
# from environments import SALT
# import hashlib

from prisma.partials import AlbumWithCover, AlbumWithMedia

api = Blueprint('', 'routes')


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
    events = db.event.find_many()
    albums = AlbumWithCover.prisma().find_many(include={"cover": True})
    people = db.people.find_many()
    gallery_cover = db.media.find_first(where={'on_gallery': True})
    about = db.about.find_first()
    return render_template('home.html', datetime=datetime, albums=albums, events=events,
                           people=people, gallery_cover=gallery_cover, about=about)


@api.get('/album/get_album_contents/<int:album_id>')
def get_album(album_id: int):
    """gets album contents"""

    album = AlbumWithMedia.prisma().find_first(
        where={'id': album_id}, include={'media': True})
    assert album is not None

    media = album.media
    has_media = len(media) > 0

    return render_template('album.html', media=media, album=album, has_media=has_media)


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


@api.get('/robots.txt')
def robots():
    """let robots access the .txt"""
    with open('robots.txt', encoding='utf-8') as file:
        contents = file.read()
    return contents
