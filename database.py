from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///database/qa.db', echo = True)
db_session = sessionmaker(bind=engine)()

Base.metadata.create_all(engine)