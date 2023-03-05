#models is used for defining a schema for our tables . With the models.py we can create the tables natively in the app and not by using admin access in pgAdmin on postgreSQL

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

#create a schema for a new table in fastApi --Posts
class Post(Base):
    __tablename__ = 'posts'
    
    id =Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable= False)
    content = Column(String, nullable=False)
    published = Column (Boolean, default=True, server_default="TRUE")
    created_at = Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()') )
    
    #foreign key to the User table
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False )
    
    #setting up the relationship to user table so that additional data can be pulled from that table
    owner = Relationship("User")

    
#table for storing users 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable= False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()') )
    

#table for votes
class Vote(Base):
    __tablename__ ="votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)
   