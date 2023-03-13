"""connect to prisma database"""
from flask import g
from prisma import Prisma


def get_db():
    """connect to the database"""
    database = getattr(g, '_database', None)
    if database is None:
        database = g._database = Prisma()
        database.connect()
    return database
