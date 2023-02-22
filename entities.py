from sqlalchemy import Column, Integer, String, Text, Boolean, Date, Time
from base import Base



class User(Base):
   __tablename__ = 'User'

   user_id = Column(Integer, primary_key = True)
   username = Column(String)
   password = Column(String)
   admin = Column(Boolean)

   def __repr__(self):
      return str((
         self.user_id, 
         self.username, 
         self.password,
         self.admin
      ))


class Event(Base):
   __tablename__ = 'Event'

   event_id = Column(Integer, primary_key = True)
   user_id = Column(Integer, foreign_key = True)
   title = Column(String)
   description = Column(Text)
   date = Column(Date)
   time = Column(Time)
   image = Column(Text)

   def __repr__(self):
      return str((
         self.event_id, 
         self.user_id, 
         self.title, 
         self.description, 
         self.date,
         self.time,
         self.image
      ))


class Media(Base):
   __tablename__ = 'Media'

   media_id = Column(Integer, primary_key = True)
   user_id = Column(Integer, foreign_key = True)
   type = Column(String)
   description = Column(Text)
   reference = Column(Text)
   date = Column(Date)

   def __repr__(self):
      return str((
         self.media_id, 
         self.user_id, 
         self.type, 
         self.description,
         self.reference,
         self.date
      ))