#!/usr/bin/env python

__author__ = "Stefan Safranek"
__copyright__ = "Copyright 2016, Social Media Automation"
__credits__ = ["Stefan Safranek"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Stefan Safranek"
__email__ = "https://github.com/sjsafranek"
__status__ = "Development"

import os
import sys
import lzma
import base64
import builtins
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
		builtins.DATABASE_PATH,
		convert_unicode=True,
		echo=False
	)

db_session = scoped_session(sessionmaker(autocommit=False,
										 autoflush=False,
										 bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


import Models


class DB(object):
	""" Database for OkCupid Model Objects """

	def __init__(self, update=False):
		""" Create database connection """
		FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
		LOG_FILENAME = os.path.join("logs","database.log")
		logging.basicConfig(
			format=FORMAT, 
			level=logging.DEBUG,
			# stream=sys.stdout,
			filename=LOG_FILENAME)
		self.logger = logging.getLogger('Database')		
		self._init_db()
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.update = update

	def _init_db(self):
		""" initiate database """
		self.logger.info("Creating tables...")
		Base.metadata.create_all(bind=engine)

	def getOkcupidUser(self, username):
		""" Retrieves user from database
			Args:
				username (str): OkCupid username
			Returns:
				User object if username is in database
				None if username not in database
		"""
		self.logger.info("Get Okcupid user: %s", username)
		user = self.session.query(Models.Okcupid).filter(Models.Okcupid.username==username).first()
		return user

	def newOkcupidUser(self, username, age, location, match, enemy, liked):
		""" Adds user to database
			Args:
				username (str): OkCupid username
				age (int): age of user
				match (float): match percentage
				liked (bool): Whether user has been `liked`
		"""
		user = self.getOkcupidUser(username)
		if not user:
			self.logger.info("Inserting new OkCupid user: %s", username)
			try:
				user = Models.Okcupid(username)
				user.age = age
				user.location = location
				user.match = match
				user.enemy = enemy
				user.liked = liked
				self.session.add(user)
				self.session.commit()
				return True
			except Exception as e:
				self.logger.error(e)
				traceback.print_stack()
				self.session.rollback()
				return False
		elif self.update:
			self.logger.info("Update existing OkCupid user: %s", username)
			try:
				user.age = age
				user.location = location
				user.match = match
				user.enemy = enemy
				user.liked = liked
				self.session.commit()
				return False
			except Exception as e:
				self.logger.error(e)
				traceback.print_stack()
				self.session.rollback()
				return False
		else:
			self.logger.info("OkCupid user already existing: %s", username)

	def getOkcupidUsers(self):
		""" Retrieves all user records from database
			Returns:
				users list(Models.Okcupid): list of User model objects 
		"""
		self.logger.info("Get all OkCupid users")
		users = self.session.query(Models.Okcupid).all()
		return users

	def getLikedOkCupidUsers(self):
		""" Retrieves liked user records from database
			Returns:
				users list(Models.Okcupid): list of User model objects 
		"""
		self.logger.info("Get all liked OkCupid users")
		users = self.session.query(Models.Okcupid).filter(Models.Okcupid.liked==True).all()
		return users

	def saveOkcupidProfile(self, username, profile_source):
		""" Save profile to database. 
			Profile linked to user in users table.
			Args:
				username (str): okcupid username
				profile_source (str): html source of profile page
		"""
		data = lzma.compress(profile_source.encode())
		encoded = base64.b64encode(data).decode('utf-8')
		user = self.getOkcupidUser(username)
		if not user:
			self.logger.info("Storing user profile: %s", username)
			user = Models.Okcupid(username)
			user.source = encoded
			self.session.add(user)
			self.session.commit()
		else:
			self.logger.info("Updating user profile: %s", username)
			user.source = encoded
			self.session.commit()

	def decodeOkcupidProfile(self, encoded):
		udatab64 = base64.b64decode(encoded)
		decoded = lzma.decompress(udatab64)
		return decoded

	def getFacebookUser(self,username):
		""" Retrieves user from database
			Args:
				username (str): Facebook username
			Returns:
				User object if username is in database
				None if username not in database
		"""
		self.logger.info("Get Facebook user: %s", username)
		user = self.session.query(Models.Facebook).filter(Models.Facebook.username==username).first()
		return user

	def createFacebookUser(self, firstname, lastname, username):
		if not self.getFacebookUser(username):
			self.logger.debug("Create Facebook user: %s", username)
			fb_user = Models.Facebook(username)
			self.session.add(fb_user)
			self.session.commit()
			# Create Person 
			person = self.createPerson(firstname, lastname)
			# Add person to facebook
			if person:
				person.profile[0].facebook.append(fb_user)
				self.session.commit()
		else:
			self.logger.debug("Facebook user exists: %s", username)

	###################################
	### CREATE PERSON AND PROFILES ###s
	###################################
	def getPerson(self, firstname, lastname):
		user = self.session.query(Models.User).filter(Models.User.firstname==firstname).filter(Models.User.lastname==lastname).first()
		return user

	def createPerson(self, firstname, lastname):
		if not self.getPerson(firstname, lastname):
			person = Models.User()
			person.firstname = firstname
			person.lastname = lastname
			self.session.add(person)
			self.session.commit()
			# Create profile
			profiles = Models.Profiles()
			self.session.add(profiles)
			self.session.commit()
			# 
			person.profile.append(profiles)
			self.session.commit()
			return person
		else:
			return None

