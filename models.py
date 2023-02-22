from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float, Date, Time
from flask_sqlalchemy import SQLAlchemy
from app import db


class User(db.Model):
  __tablename__ = 'User'
  
  user_id = Column(Integer, primary_key = True)
  username = Column(String)
  password = Column(String)
  admin = Column(Boolean)
  
  def __repr__(self):
    return 'User: {}'.format(self.username)


class Event(db.Model):
   __tablename__ = 'Event'

   event_id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('User.user_id'), nullable = False)
   title = Column(String)
   description = Column(Text)
   date = Column(Date)
   time = Column(Time)
   image = Column(Text)

   def __repr__(self):
    return 'Event: {}'.format(self.title)


class Media(db.Model):
   __tablename__ = 'Media'

   media_id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('User.user_id'), nullable = False)
   type = Column(String)
   description = Column(Text)
   reference = Column(Text)
   date = Column(Date)



# class User(Base):
#    __tablename__ = 'User'

#    user_id = Column(Integer, primary_key = True)
#    username = Column(String)
#    password = Column(String)
#    admin = Column(Boolean)

#    def __repr__(self):
#       return str((
#          self.user_id, 
#          self.username, 
#          self.password,
#          self.admin
#       ))


# class Event(Base):
#    __tablename__ = 'Event'

#    event_id = Column(Integer, primary_key = True)
#    user_id = Column(Integer, foreign_key = True)
#    title = Column(String)
#    description = Column(Text)
#    date = Column(Date)
#    time = Column(Time)
#    image = Column(Text)

#    def __repr__(self):
#       return str((
#          self.event_id, 
#          self.user_id, 
#          self.title, 
#          self.description, 
#          self.date,
#          self.time,
#          self.image
#       ))


# class Media(Base):
#    __tablename__ = 'Media'

#    media_id = Column(Integer, primary_key = True)
#    user_id = Column(Integer, foreign_key = True)
#    type = Column(String)
#    description = Column(Text)
#    reference = Column(Text)
#    date = Column(Date)

#    def __repr__(self):
#       return str((
#          self.media_id, 
#          self.user_id, 
#          self.type, 
#          self.description,
#          self.reference,
#          self.date
#       ))