import random

from bson.objectid import ObjectId
from pymongo import DESCENDING
from app import db


class GameDAO(object):
    _db = db

    def get_all_stars(self):
        return list(self._db.stars.find())

    def get_random_star(self):
        total_stars = self._db.stars.count()
        if total_stars:
            random_entry = random.randint(1, total_stars)
            random_star = self._db.stars.find().limit(-1).\
                skip(random_entry).next()
            return random_star

    def get_top_games(self):
        games = db.games.find().limit(10).sort('correct', DESCENDING)
        top_games = []
        for game in games:
            player = db.players.find_one({'_id': ObjectId(game['player_id'])})
            top_games.append(
                {
                    'correct': game['correct'],
                    'failed': game['failed'],
                    'player': player['name'],
                    'start_time': game['start_time']
                }
            )
        return top_games

    @property
    def can_play(self):
        return self.count >= 8

    @property
    def count(self):
        return self._db.stars.count()
