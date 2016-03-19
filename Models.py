#!/usr/bin/python

import datetime
import builtins
# from Database import Base
from sqlalchemy import ForeignKey
# from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


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


class User(Base):
    """ users table """
    __tablename__ = 'users'
    uuid = Column(Integer, primary_key=True)
    firstname = Column(String(50), unique=False)
    lastname = Column(String(50), unique=False)
    age = Column(Integer, unique=False)
    # created_date = Column(DateTime, default=func.now())
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    profile = relationship("Profiles", backref="profiles")

    def __repr__(self):
        return '<%r %r>' % (self.firstname, self.lastname)


class Profiles(Base):
    """ profile table """
    __tablename__ = 'profiles'
    uuid = Column(Integer, primary_key=True)
    # facebook = Column(String(50), unique=True)
    # okcupid = Column(String(50), unique=True)
    # twitter = Column(String(50), unique=True)
    # linkedin = Column(String(50), unique=True)
    facebook = relationship("Facebook", backref="facebook")
    okcupid = relationship("Okcupid", backref="okcupid")
    twitter = relationship("Twitter", backref="twitter")
    # linkedin = relationship("Linkedin", backref="linkedin")
    user_id = Column(Integer, ForeignKey('users.uuid'))

    def __repr__(self):
        return '<facebook: %r, okcupid: %r, twitter: %r>' % (self.facebook, self.okcupid, self.twitter)


class Okcupid(Base):
    """ okcupid table """
    __tablename__ = 'okcupid'
    uuid = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    location = Column(String(50), unique=False)
    age = Column(Integer, unique=False)
    match = Column(Float, unique=False)
    enemy = Column(Float, unique=False)
    liked = Column(Boolean, unique=False)
    source = Column(String, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    profile = Column(Integer, ForeignKey('profiles.uuid'))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<Okcupid User %r>' % (self.username)


class Facebook(Base):
    """ facebook table """
    __tablename__ = 'facebook'
    uuid = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    location = Column(String(50), unique=False)
    age = Column(Integer, unique=False)
    source = Column(String, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    profile = Column(Integer, ForeignKey('profiles.uuid'))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<Facebook User %r>' % (self.username)


class Twitter(Base):
    """ twitter table """
    __tablename__ = 'twitter'
    uuid = Column(Integer, primary_key=True)
    handle = Column(String(50), unique=True)
    firstname = Column(String(150), unique=False)
    lastname = Column(String(150), unique=False)
    location = Column(String(150), unique=False)
    website = Column(String(150), unique=False)
    bio = Column(String(300), unique=False)
    tweets = relationship("Tweet", backref="tweets")
    profile = Column(Integer, ForeignKey('profiles.uuid'))

    def __init__(self, handle):
        self.handle = handle

    def __repr__(self):
        return '<Twitter handle %r>' % (self.handle)

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    handle = Column(String(50), unique=False)
    tweet_time = Column(DateTime, unique=False)
    text = Column(String(150), unique=False)
    dtype = Column(String(50), unique=False)
    itemid = Column(String(120), unique=False)
    retweets = Column(Integer, unique=False)
    favorites = Column(Integer, unique=False)
    status = Column(Integer, unique=False)
    handler_id = Column(Integer, ForeignKey("twitter.uuid"))
    Timestamp =Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, twitter_handle=None, tweet_time=None, tweet_text=None, data_type=None, data_id=None, retweets=None, favorites=None, status=None):
        self.handle = twitter_handle
        self.tweet_time = tweet_time
        self.text = tweet_text
        self.dtype = data_type
        self.itemid = str(data_id)
        self.retweets = int(retweets)
        self.favorites = int(favorites)
        self.status = status

    def __repr__(self):
        return '<Tweet %r>' % (self.tweet_text)