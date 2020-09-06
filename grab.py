# -*- coding: utf-8 -*-
import re
import json
import time

from flask import Blueprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from app import db
from app import application as app


def setup_capabilities():
    capabilities = DesiredCapabilities.PHANTOMJS.copy()
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = '159.8.114.34:8123'
    # prox.socks_proxy = "ip_addr:port"
    # prox.ssl_proxy = "ip_addr:port"
    proxy.add_to_capabilities(capabilities)

    return capabilities


HOST_BASE = 'https://kinopoisk.ru/'
"""
https://kinopoisk.ru/images/lg_actor/38702.jpg
https://st.kp.yandex.net/images/actor_iphone/iphone360_38702.jpg
"""

def grab_to_database():
    # from selenium.webdriver.chrome.options import Options
    # driver = webdriver.PhantomJS(desired_capabilities=setup_capabilities())
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # proxy_uri = f'https://{app.config["PROXY_HOST"]}:{app.config["PROXY_PORT"]}'
    # chrome_options.add_argument(f'--proxy-server={proxy_uri}')
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome()

    driver.get(HOST_BASE)
    login_button = driver.find_element_by_xpath('//button[text()="Войти"]')
    login_button.click()
    login_element = driver.find_element_by_name('login')
    login_element.send_keys(app.config['YANDEX_USER'])
    button_element = driver.\
        find_element_by_css_selector('button[type=submit].Button2_type_submit')
    button_element.click()
    time.sleep(1)
    password_element = driver.find_element_by_name('passwd')
    password_element.send_keys(app.config['YANDEX_PASS'])
    # Stale button is not available anymore
    button_element_new = driver.\
        find_element_by_css_selector('button[type=submit].Button2_type_submit')
    button_element_new.click()
    app.logger.info('Waiting for login...')
    time.sleep(2)

    driver.get(f'{HOST_BASE}mykp/stars/')
    html = driver.page_source
    start_page_html = BeautifulSoup(html)
    persons = []  # all persons find in my kinopoisk profile

    # first find all folders
    folder_list = start_page_html.find(id='folderList')
    folders = folder_list.find_all('li')
    for folder in folders:
        folder_id = folder['data-id']
        driver.get(f'{HOST_BASE}mykp/stars/list/type/{folder_id}')
        html = driver.page_source
        parsed_html = BeautifulSoup(html)
        category_elem = parsed_html.select('input[name=folder_name]')
        category_name = category_elem[0]['value']
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

        # iterate pages within category
        for page in range(last_page):
            app.logger.debug(f'Processing page #{page+1}...')
            route = f'{HOST_BASE}mykp/stars/list/type/{folder_id}/page/{page+1}/'
            driver.get(route)
            page_html = BeautifulSoup(driver.page_source)
            stars_list = page_html.find_all(id=re.compile('^people'))
            stars = [item.find('a', text=True, class_='name').text
                     for item in stars_list]
            for item in stars_list:
                person_id = item['data-id']
                name = item.find('a', text=True, class_='name').text
                orig_name_elem = item.find('span', text=True)
                orig_name = name if orig_name_elem is None \
                    else orig_name_elem.text

                record_id = 'person' + str(person_id)
                persons.append({
                    'id': person_id,
                    'name': name,
                    'category': category_name
                })
                new_person = {
                    'id': person_id,
                    'name': name,
                    'orig_name': orig_name,
                    'category': category_name,
                }
                db.stars.insert_one(new_person)
    app.logger.info('Done')


if __name__ == '__main__':
    grab_to_database()