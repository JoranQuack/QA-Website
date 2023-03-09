from sqlalchemy import Column as Col, Integer, Text, Boolean, Date, Time, ForeignKey
from database import Base



class Column(Col):
   def __init__(sel, *args, **kwargs):
      kwargs.setdefault('nullable', False)
      super().__init__(*args, **kwargs)



class User(Base):
   __tablename__ = 'User'

   id = Column(Integer, primary_key = True)
   username = Column(Text)
   password = Column(Text)
   admin = Column(Boolean)

   def __repr__(self):
      return str((
         self.id, 
         self.username, 
         self.password,
         self.admin
      ))


class Event(Base):
   __tablename__ = 'Event'

   id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('User.id'))
   title = Column(Text)
   description = Column(Text)
   date = Column(Date)
   time = Column(Time, nullable = True)

   def __repr__(self):
      return str((
         self.id, 
         self.user_id, 
         self.title, 
         self.description, 
         self.date,
         self.time
      ))
   

class About(Base):
   __tablename__ = 'About'

   id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('User.id'))
   description = Column(Text)
   location = Column(Text)

   def __repr__(self):
      return str((
         self.id, 
         self.user_id,
         self.description,
         self.location
      ))
   

class People(Base):
   __tablename__ = 'People'

   id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('User.id'))
   reference = Column(Text)
   name = Column(Text)
   role = Column(Text, nullable = True)

   def __repr__(self):
      return str((
         self.id, 
         self.user_id, 
         self.reference, 
         self.name,
         self.role
      ))


class Album(Base):
   __tablename__ = 'Album'

   id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('User.id'))
   title = Column(Text)
   description = Column(Text)

   def __repr__(self):
      return str((
         self.id, 
         self.user_id, 
         self.title, 
         self.description
      ))


class Media(Base):
   __tablename__ = 'Media'

   id = Column(Integer, primary_key = True)
   user_id = Column(Integer, ForeignKey('User.id'))
   album_id = Column(Integer, ForeignKey('Album.id'))
   type = Column(Text)
   reference = Column(Text)
   description = Column(Text)

   def __repr__(self):
      return str((
         self.id, 
         self.user_id, 
         self.type,
         self.reference,
         self.description
      ))