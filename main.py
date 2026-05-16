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


def fetch_website(link, timeout):

    try:
        response = session.get(link, timeout=timeout)
        response.raise_for_status()
        logger.info('Success! The website has been successfully fetched from the server...\n')
        logger.info(f'Target Site: {response.url}')
        logger.info(f'Status Code: {response.status_code}\n')

    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP Request Error Occured! Status Code: {e.response.status_code} | {e.response.url}')


cookies = {}


def browser_cookies():

    if not os.path.exists('cookies.json'):
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f, indent=4)

        logger.info(f'Cookies assigned to us: {len(session.cookies)}\n')

    for x, y in session.cookies.items():
        logger.info(f'{x}: {y}')
        cookies[x] = y
    logger.info('\n')

    logger.info('Cookies has been saved to a "cookies.json" file in the local directory!\n')


if os.path.exists('cookies.json'):

    with open('cookies.json', 'r') as f:
        reuse_cookies = json.load(f)
        session.cookies.update = httpx.Cookies(reuse_cookies)

    logger.info('"Cookies.json" file exists! Reloading cookies...\n')


fetch_website(url, 120)
browser_cookies()
session.close()
