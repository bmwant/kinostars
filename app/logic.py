import json
import random

from app import db, redis_db


def generate_game(player_id, category, variants=6):
    """
    Generate whole game from mongo and write it to redis
    """
    persons = list(db.stars.find({'category': {'$in': category}}))
    total_games = len(persons)
    random.shuffle(persons)
    game = [p['id'] for p in persons]
    redis_db.hset(player_id, 'game', json.dumps(game))
    redis_db.hset(player_id, 'total_games', total_games)
    redis_db.hset(player_id, 'level_variants', variants)


def get_level(player_id, level):  # unicode, int
    total_games = (redis_db.hget(player_id, 'total_games'))
    variants = int(redis_db.hget(player_id, 'level_variants'))
    if level >= total_games:
        return None
    rr = json.loads(redis_db.hget(player_id, 'game'))
    level_person = rr[level-1]
    correct_person = db.stars.find_one({'id': level_person})

    all_persons = list(db.stars.find({'category': correct_person['category']}))
    random.shuffle(all_persons)
    persons = all_persons[:variants]
    if correct_person not in persons:
        position = random.randint(1, variants)
        persons[position-1] = correct_person

    photo = correct_person['photo']
    category = correct_person['category']
    # random.shuffle(persons)
    return {
        'photo': photo,
        'persons': persons,
        'category': category
    }


def check_answer(player_id, level, answer):  # unicode, int, unicode
    """
    Checks if the answer of player for the level is correct
    """
    level_person = json.loads(redis_db.hget(player_id, 'game'))[level-1]
    if level_person == answer:
        return True
    return False


def get_answer(player_id, level):  # unicode, int
    """
    Returns correct star id at the level for the player
    """
    return json.loads(redis_db.hget(player_id, 'game'))[level-1]
