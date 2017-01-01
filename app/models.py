from app import db


class GameDAO(object):
    _db = db

    def get_all_stars(self):
        return list(self._db.stars.find())
