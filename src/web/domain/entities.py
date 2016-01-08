import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	social_id = Column(String(64), nullable=False, unique=True)
	username = Column(String(100), nullable=False)
	email = Column(String(100), nullable=False)

	@property
	def serialize(self):
		"""User in a serialized format"""
		return {
		'social_id': self.social_id,
		'id': self.id,
		'username': self.username,
		'email': self.email
		}

class Profile(Base):
	"""Profile Table"""
	__tablename__ = "profiles"
	id = Column(Integer, primary_key=True)
	url = Column(String(1000))
	createdDate = Column(DateTime, default=datetime.datetime.utcnow)
	active = Column(Boolean, default=True)

	@property
	def  serialize(self):
		"""Profile in serialized format"""
		return{
		'id': self.id,
		'url': self.url,
		'createdDate' : self.createdDate,
		'active': self.active
		}

engine = create_engine('sqlite:///../../database/myweb.db')
Base.metadata.create_all(engine)