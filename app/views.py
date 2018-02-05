# -*- coding: utf-8 -*-
import json
import datetime

from flask import (render_template, request, g, redirect, session,
                   make_response, url_for)
from bson.objectid import ObjectId
from app import db, redis_db
from app import application as app
from auxiliary import requires_auth
from models import GameDAO
from logic import get_answer, generate_game, get_level, check_answer


@app.route('/all')
@requires_auth
def saved_stars():
    stars = g.db.get_all_stars()
    return render_template('names.html', stars=stars)


@app.route('/admin')
@requires_auth
def admin_panel():
    return render_template('admin.html')


@app.before_request
def load_all_persons():
    # todo: add validations for invalid records in cookies
    g.authenticated = 'player_id' in request.cookies
    g.username = request.cookies.get('name', u'Гость')
    g.current_year = datetime.datetime.now().year
    g.db = GameDAO()


@app.route('/')
def index():
    person = g.db.get_random_star()
    return render_template('index.html', person=person)


@app.route('/statistic')
def statistic():
    """
    Get statistic for player games
    """
    player_id = request.cookies['player_id']
    player = db.players.find_one({'_id': ObjectId(player_id)})
    games = [db.games.find_one({'_id': game_id})
             for game_id in player['games']]
    # todo: select sorted by date and limit to 20 records
    games = games[:20]
    return render_template('statistic.html', games=games, name=player['name'])


@app.route('/records')
def records():
    player_id = request.cookies.get('player_id')
    top_games = g.db.get_top_games()
    return render_template('records.html',
                           games=top_games,
                           player_id=player_id)


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    cookies_data = (
        'time',
        'variants',
        'name',
        'player_id',
        'actors',
        'actress',
        'director',
        'errors',
    )
    for cookie in cookies_data:
        resp.set_cookie(cookie, '', expires=0)

    return resp


@app.route('/endgame')
def end():
    player_id = request.cookies['player_id']
    redis_db.delete(player_id)
    return 'Ok'


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'GET':
        if 'player_id' in request.cookies:
            # Player wants to play another game and we know him
            player_id = request.cookies['player_id']
            player = db.players.find_one({'player_id': player_id})
        else:
            # It is new player, create account for him
            player_id = db.players.insert({'name': g.username, 'games': []})

        actors = request.cookies['actors']
        actress = request.cookies['actress']
        director = request.cookies['director']
        cats = []  # that's dumb
        if actors == u'1':
            cats.append(u'Актёры')
        if actress == u'1':
            cats.append(u'Актрисы')
        if director == u'1':
            cats.append(u'Режиссеры')

        # Generate game and store it in redis for current user
        generate_game(player_id,
                      category=cats,
                      variants=int(request.cookies['variants']))
        level_data = get_level(player_id, 1)

        # and create mongo db session for this game
        new_game = {
            'correct': 0,
            'level': 1,
            'failed': 0,
            'start_time': datetime.datetime.now(),
            'player_id': player_id
        }
        game_id = db.games.insert(new_game)
        db.players.update({'_id': ObjectId(player_id)},
                          {'$addToSet': {'games': game_id}})
        session['game_id'] = str(game_id)

        app.logger.info('Starting game for player {}'.format(player_id))
        # Return page with first level
        resp = make_response(render_template('game.html', **level_data))
        resp.set_cookie('player_id', str(player_id), max_age=60*60*24*12*5)
        return resp

    if request.method == 'POST':
        # continue game with ajax-requests
        game_id = session['game_id']  # what is the game

        games = db.games
        current_game = games.find_one({'_id': ObjectId(game_id)})

        player_id = current_game['player_id']
        app.logger.info('Resuming game for player {}'.format(player_id))
        answer = request.form['id']
        current_level = int(current_game['level'])

        if check_answer(player_id, current_level, answer):
            # correct answer
            current_game['correct'] += 1
        else:
            current_game['failed'] += 1

        allowed = int(request.cookies['errors'])
        level_data = get_level(player_id, current_level+1)
        cause = False
        if allowed != 123 and current_game['failed'] >= allowed:
            cause = 'limit'
        if level_data is None:
            cause = 'end'

        if cause:
            # Game over
            return json.dumps({
                'statistic': {
                    'correct': current_game['correct'],
                    'failed': current_game['failed']
                },
                'previous': {
                    'right': get_answer(player_id, current_level),
                    'yours': answer
                },
                'over': cause
            })
        else:
            current_game['level'] += 1  # go to the next level

        games.save(current_game)  # write changes back to mongodb

        persons = [{
            'id': person['id'],
            'name': person['name']
        } for person in level_data['persons']]

        return json.dumps({
            'photo': level_data['photo'],
            'category': level_data['category'],
            'persons': persons,
            'statistic': {
               'correct': current_game['correct'],
               'failed': current_game['failed']
            },
            'previous': {
               'right': get_answer(player_id, current_level),
               'yours': answer
            },
            'over': False
        })
