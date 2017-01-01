# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from flask import Flask
from .config import DevelopmentConfig

application = Flask(__name__)

application.config.from_object(DevelopmentConfig)

# Initialize db here. You already can use config
from redis import Redis
redis_db = Redis()

from pymongo import MongoClient
mongo_client = MongoClient(application.config['DB_URI'])
db = mongo_client.game_db

# Register blueprints here
from grabber.kinopoisk_grab import kinopoisk_agent
application.register_blueprint(kinopoisk_agent)

# Import views here
import app.views
