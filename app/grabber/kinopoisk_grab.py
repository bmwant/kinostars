# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from flask import Blueprint, render_template, abort, request, g, redirect, \
    session, g, make_response
from twill.commands import go, show, clear_cookies, fv, submit
from bs4 import BeautifulSoup
import re
import random
import json
import uuid
from bson.objectid import ObjectId
import datetime


kinopoisk_agent = Blueprint('kinopoisk_agent', __name__,
                            template_folder='templates')


from pymongo import MongoClient, DESCENDING
mongo_client = MongoClient('mongodb://127.0.0.1:27017')
db = mongo_client.game_db

#from auxiliary import requires_auth



#@requires_auth
def grab():
    """
    Function that grab all start from your kinopoisk account and
    write them to redis store
    """
    clear_cookies()

    go('http://kinopoisk.ru/login/')
    fv(2, "shop_user[login]", "bmwant21")
    fv(2, "shop_user[pass]", "M17wayt0B@d")
    submit('0')

    go('http://www.kinopoisk.ru/mykp/stars/')
    html = show()
    start_page_html = BeautifulSoup(html)
    persons = []  # all persons find in my kinopoisk profile

    # first find all folders
    folder_list = start_page_html.find(id='folderList')
    folders = folder_list.find_all('li')
    for folder in folders:
        folder_id = folder['data-id']
        go('http://www.kinopoisk.ru/mykp/stars/list/type/%s' % folder_id)
        html = show()
        parsed_html = BeautifulSoup(html)
        input = parsed_html.select('input[name=folder_name]')
        category_name = input[0]['value']

        # if there is no persons in such category
        if parsed_html.find(class_='emptyMessage'):
            # skip it
            continue

        # go through all pages of this category
        all_arrows = parsed_html.find_all(class_='arr')
        if all_arrows:
            last_link = all_arrows[-1].find('a')['href']
            last_page = int(re.findall(r'\d+', last_link)[-1])
        else:
            last_page = 1

        for page in range(last_page):
            route = 'http://www.kinopoisk.ru/mykp/stars/list/type/%s/page/%s/' % (folder_id, (page+1))
            go(route)
            page_html = BeautifulSoup(show())
            stars_list = page_html.find_all(id=re.compile('^people'))
            stars = [item.find('a', text=True, class_='name').text
                     for item in stars_list]
            for item in stars_list:
                person_id = item['data-id']
                name = item.find('a', text=True, class_='name').text
                #add newly grabbed person to redis store
                record_id = 'person' + str(person_id)
                persons.append({'name': name, 'id': person_id, 'category': category_name})
                redis.hset(record_id, 'name', name)
                redis.hset(record_id, 'id', person_id)
                redis.hset(record_id, 'category', category_name)
                redis.hset(record_id, 'photo',
                           'http://st.kp.yandex.net/images/'
                           'actor_iphone/iphone360_%s.jpg' % person_id)
    return render_template("names.html", stars=persons)

def grab_photos():
    pass

@kinopoisk_agent.route('/grab')
def grab_to_mongo():
    """
    Function that grab all start from your kinopoisk account and
    write them to redis store
    """
    clear_cookies()

    go('http://kinopoisk.ru/login/')
    fv(2, "shop_user[login]", "bmwant21")
    fv(2, "shop_user[pass]", "M17wayt0B@d")
    submit('0')

    go('http://www.kinopoisk.ru/mykp/stars/')
    html = show()
    start_page_html = BeautifulSoup(html)
    persons = []  # all persons find in my kinopoisk profile

    # first find all folders
    folder_list = start_page_html.find(id='folderList')
    folders = folder_list.find_all('li')
    for folder in folders:
        folder_id = folder['data-id']
        go('http://www.kinopoisk.ru/mykp/stars/list/type/%s' % folder_id)
        html = show()
        parsed_html = BeautifulSoup(html)
        input = parsed_html.select('input[name=folder_name]')
        category_name = input[0]['value']

        # if there is no persons in such category
        if parsed_html.find(class_='emptyMessage'):
            # skip it
            continue

        # go through all pages of this category
        all_arrows = parsed_html.find_all(class_='arr')
        if all_arrows:
            last_link = all_arrows[-1].find('a')['href']
            last_page = int(re.findall(r'\d+', last_link)[-1])
        else:
            last_page = 1

        for page in range(last_page):
            route = 'http://www.kinopoisk.ru/mykp/stars/list/type/%s/page/%s/' % (folder_id, (page+1))
            go(route)
            page_html = BeautifulSoup(show())
            stars_list = page_html.find_all(id=re.compile('^people'))
            stars = [item.find('a', text=True, class_='name').text
                     for item in stars_list]
            for item in stars_list:
                person_id = item['data-id']
                name = item.find('a', text=True, class_='name').text
                #add newly grabbed person to redis store
                record_id = 'person' + str(person_id)
                persons.append({'name': name, 'id': person_id, 'category': category_name})
                # and create mongo db session for this game
                new_person = {
                    'id': person_id,
                    'name': name,
                    'category': category_name,
                    'photo': 'http://st.kp.yandex.net/images/'
                             'actor_iphone/iphone360_%s.jpg' % person_id
                }
                new_person_id = db.stars.insert(new_person)
    return 'Ok'


@kinopoisk_agent.route('/redname')
#@requires_auth
def saved_stars():
    """
    There is no need to reload all stars from kinopoisk site because
    we've cached them with redis
    """
    #for r in records:
    #    print '%s - > %s' % (redis.hget(r, 'id'), redis.hget(r, 'name'))
    return render_template("names.html", stars=g.all_persons)











