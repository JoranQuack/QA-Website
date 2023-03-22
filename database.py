"""connect to prisma database"""
from prisma import Prisma

database = Prisma()
database.connect()
