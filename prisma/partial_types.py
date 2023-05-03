'''Prisma partial type generation'''
from prisma.models import Album, Media

Album.create_partial('AlbumWithCover', required={'cover'})
Album.create_partial('AlbumWithMedia', required={'media'})
Media.create_partial('MediaWithAlbums', required={'albums'})
