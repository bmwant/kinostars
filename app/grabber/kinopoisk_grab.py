# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
from flask import (Blueprint, render_template, abort, request, g, redirect,
                   make_response)
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

from app import db
from app.auxiliary import requires_auth


@kinopoisk_agent.route('/grab_photos')
@requires_auth
def grab_photos():
    return 'Ok'


@kinopoisk_agent.route('/grab')
@requires_auth
def grab_to_mongo():
    """
    Function that grab all start from your kinopoisk account and
    write them to mongo database
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











