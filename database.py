# pylint: disable=no-name-in-module
"""connect to prisma database"""
from prisma import Prisma

database = Prisma()
database.connect()
