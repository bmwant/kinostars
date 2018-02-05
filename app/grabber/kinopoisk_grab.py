# -*- coding: utf-8 -*-
import re
import time

from flask import Blueprint
from bs4 import BeautifulSoup
from selenium import webdriver


kinopoisk_agent = Blueprint('kinopoisk_agent', __name__,
                            template_folder='templates')

from app import db
from app.auxiliary import requires_auth
from app import application as app


@kinopoisk_agent.route('/test')
@requires_auth
def grab_photos():
    return 'Ok'


@kinopoisk_agent.route('/check_state')
def check_updating_state():
    pass


@kinopoisk_agent.route('/grab')
@requires_auth
def grab_to_mongo():
    """
    Function that grab all start from your kinopoisk account and
    write them to mongo database
    """
    app.logger.debug('Initializing web driver')
    driver = webdriver.PhantomJS()
    driver.get('http://kinopoisk.ru/login/')
    driver.switch_to_frame('kp2-authapi-iframe')
    time.sleep(1)
    login_element = driver.find_element_by_name('login')
    password_element = driver.find_element_by_name('password')
    login_element.send_keys(app.config['KINOPOISK_USER'])
    time.sleep(1)
    password_element.send_keys(app.config['KINOPOISK_PASS'])
    time.sleep(1)
    button_element = driver.\
        find_element_by_css_selector('button[type=submit].auth__signin')
    app.logger.debug('Login into account')
    button_element.click()
    time.sleep(3)
    driver.get('http://www.kinopoisk.ru/mykp/stars/')
    html = driver.page_source
    start_page_html = BeautifulSoup(html)
    persons = []  # all persons find in my kinopoisk profile

    # first find all folders
    folder_list = start_page_html.find(id='folderList')
    folders = folder_list.find_all('li')
    for folder in folders:
        folder_id = folder['data-id']
        driver.get('http://www.kinopoisk.ru/'
                   'mykp/stars/list/type/{}'.format(folder_id))
        html = driver.page_source
        parsed_html = BeautifulSoup(html)
        input = parsed_html.select('input[name=folder_name]')
        category_name = input[0]['value']
        app.logger.debug(u'Inspecting category {}...'.format(category_name))
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
            app.logger.debug('Processing page {}...'.format(page+1))
            route = 'http://www.kinopoisk.ru/mykp/stars/list/type/' \
                '{folder_id}/page/{page_number}/'.format(folder_id=folder_id,
                                                         page_number=page+1)
            driver.get(route)
            page_html = BeautifulSoup(driver.page_source)
            stars_list = page_html.find_all(id=re.compile('^people'))
            stars = [item.find('a', text=True, class_='name').text
                     for item in stars_list]
            for item in stars_list:
                person_id = item['data-id']
                name = item.find('a', text=True, class_='name').text
                record_id = 'person' + str(person_id)
                persons.append({
                    'id': person_id,
                    'name': name,
                    'category': category_name
                })
                new_person = {
                    'id': person_id,
                    'name': name,
                    'category': category_name,
                    'photo': 'http://st.kp.yandex.net/images/'
                             'actor_iphone/iphone360_%s.jpg' % person_id
                }
                new_person_id = db.stars.insert(new_person)
    app.logger.info('Database updated')
    return 'Ok'
