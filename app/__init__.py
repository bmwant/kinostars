# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from flask import Flask
from .config import DevelopmentConfig

application = Flask(__name__)

application.config.from_object(DevelopmentConfig)

#initialize db here. You already can user config
from redis import Redis
redis_db = Redis()

from pymongo import MongoClient
mongo_client = MongoClient('mongodb://127.0.0.1:27017')
db = mongo_client.game_db

#register blueprints here
from grabber.kinopoisk_grab import kinopoisk_agent
application.register_blueprint(kinopoisk_agent)


#import views here
import app.views