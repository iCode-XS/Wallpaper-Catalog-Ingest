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


def fetch_website(link, timeout):   # Fetching the website from the server

    try:
        response = session.get(link, timeout=timeout)
        response.raise_for_status()
        logger.info('Success! The website has been successfully fetched from the server...\n')
        logger.info(f'Target Site: {response.url}')
        logger.info(f'Status Code: {response.status_code}\n')

    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP Request Error Occured! Status Code: {e.response.status_code} | {e.response.url}')


cookies = {}


def browser_cookies():  # This function looks and saves the cookies in a 'cookie.json' file - presented by a server

    if not os.path.exists('cookies.json'):  # This if statement is checking if 'cookie.json' file exists or not
        with open('cookies.json', 'w') as f:    # If it doesn't exist, it will save all the cookies in a 'cookie.json' file
            json.dump(cookies, f, indent=4)     # If it does exist then this entire block will not run by python

        logger.info(f'Cookies assigned to us: {len(session.cookies)}\n')

        for x, y in session.cookies.items():
            logger.info(f'{x}: {y}')
            cookies[x] = y

        logger.info('\n')
        logger.info('Cookies has been saved to a "cookies.json" file in the local directory!\n')


if os.path.exists('cookies.json'):  # This if statement is checking if a 'cookies.json' file exists or not

    with open('cookies.json', 'r') as f:    # If that file exists then it will reuse the cookies
        reuse_cookies = json.load(f)        # If not then this will not run by python
        session.cookies.update(httpx.Cookies(reuse_cookies))

    logger.info('"Cookies.json" file exists! Reloading cookies...\n')
    for x, y in session.cookies.items():
        logger.info(f'{x}: {y}')
    logger.info('\n')

fetch_website(url, 120)
browser_cookies()
session.close()
