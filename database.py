"""connect to prisma database"""
from prisma import Prisma

db = Prisma(auto_register=True)
db.connect()
