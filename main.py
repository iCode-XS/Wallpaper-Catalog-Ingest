#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup
from loguru import logger
import user_agents
import json
import os

logger.add('scraper.log', rotation='10 MB')


url = 'https://www.yorkwallcoverings.com/wallpaper-york'

session = httpx.Client(headers=user_agents.chromium_linux, http2=True)


@logger.catch
def fetch_website(link, timeout):   # Fetching the website from the server

    try:
        response = session.get(link, timeout=timeout)
        response.raise_for_status()
        logger.info('Success! The website has been successfully fetched from the server...\n')
        logger.info(f'Target Site: {response.url}')
        logger.info(f'Status Code: {response.status_code}\n')
        return response

    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP Request Error Occured! Status Code: {e.response.status_code} | {e.response.url}')


cookies = {}


def browser_cookies():  # This function looks and saves the cookies in a 'cookie.json' file - presented by the server

    if not os.path.exists('cookies.json'):  # This if statement is checking if 'cookie.json' file exists or not

        with open('cookies.json', 'w') as f:    # If it doesn't exist, it will save all the cookies in a 'cookie.json' file
            json.dump(cookies, f, indent=4)

        logger.info(f'Cookies assigned to us: {len(session.cookies)}\n')

        for x, y in session.cookies.items():
            logger.info(f'{x}: {y}')
            cookies[x] = y

        logger.info('\n')
        logger.info('Cookies has been saved to a "cookies.json" file in the local directory!\n')


@logger.catch
def parsing_site(httpx_object):
    try:
        soup = BeautifulSoup(response, 'lxml')
        logger.info('Parsing has been successful!\n')
        return soup

    except Exception as e:
        logger.critical('The parsing of HTML document has been failed... The script will not be able to hold without this function!', e)


def main_page_ingest(bs4_object, list_name):
    item_box = bs4_object.find_all('div', class_='item-box')
    print('Number of items in the page:', len(item_box))
    print('\n')
    print('York Wallcoverings Wallpaper Catalog Showcase:\n')
    print('\n')

    for x in item_box:
        title_container = x.find('h3', class_='product-title')
        title = title_container.find('a').text
        price_container = x.find('div', class_='prices')
        price = price_container.find('span', class_='price actual-price avoid-wrap').text
        actual_price = price.strip('Actual Price:USD ')

        product_container = x.find('div', class_='picture')
        product_link = product_container.find('a')['href']

        product_id = x.find('div', class_='product-item ViewProduct').get('data-productid', 'N/A')


        base_url = 'https://www.yorkwallcoverings.com'

        print('Name:', title)
        print('Price:', actual_price)
        print('Link:', base_url + product_link)
        print('Product ID:', product_id)
        print('\n')

        list_name.append(base_url + product_link) 


def link_harvester():
    pass


def product_page_ingest(links_list):

    while links_list:

        popped_url = links_list.pop(0)
        current_url = popped_url
        print('Popped_URL:', current_url)
        print('\n')
        product_page = fetch_website(current_url, 30)
        product_page_parse = parsing_site(product_page)

        with open('product.html', 'w', encoding='utf-8') as f:

            f.write(product_page_parse.prettify())

        print('Your .html has been saved successfully!')

        break


if os.path.exists('cookies.json'):  # This if statement is checking if a 'cookies.json' file exists or not

    with open('cookies.json', 'r') as f:    # If that file exists then it will reuse the cookies
        reuse_cookies = json.load(f)
        session.cookies.update(httpx.Cookies(reuse_cookies))

    logger.info('"Cookies.json" file exists! Reloading cookies...\n')
    for x, y in session.cookies.items():
        logger.info(f'{x}: {y}')
    logger.info('\n')


product_website = []

response = fetch_website(url, 120)
browser_cookies()
soup = parsing_site(response)
wallpaper = main_page_ingest(soup, product_website)


session.close()
