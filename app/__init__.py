# -*- coding: utf-8 -*-
import config
import logging

from flask import Flask
from redis import Redis
from pymongo import MongoClient

application = Flask(__name__)

application.config.from_object(config)

redis_db = Redis(host=application.config['REDIS_HOST'],
                 port=application.config['REDIS_PORT'])


mongo_client = MongoClient(application.config['MONGO_URI'])
db = mongo_client.game_db

formatter = logging.Formatter('%(asctime)s :: line %(lineno)d, %(module)s '
                              '[%(levelname)s] %(message)s')
formatter.datefmt = '%H:%M:%S %d/%m/%y'
application.logger.handlers[0].setFormatter(formatter)

# Register blueprints here
from grabber.kinopoisk_grab import kinopoisk_agent
application.register_blueprint(kinopoisk_agent)

# Import views here
import app.views
