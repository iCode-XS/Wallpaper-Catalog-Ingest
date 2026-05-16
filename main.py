#!/usr/bin/env python3


import httpx
from bs4 import BeautifulSoup
from loguru import logger
import user_agents 

logger.add('scraper.log', rotation='10 MB')


url = 'https://www.yorkwallcoverings.com/wallpaper-york'

session = httpx.Client(headers=user_agents.chromium_linux, http2=True)


def fetch_website(link, timeout):

    try:
        response = session.get(link, timeout=timeout)
        response.raise_for_status()
        logger.info('Success! The website has been successfully fetched from the server...\n')
        logger.info(f'Target Site: {response.url}')
        logger.info(f'Status Code: {response.status_code}')

    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP Request Error Occured! Status Code: {e.response.status_code} | {e.response.url}')


fetch_website(url, 120)
session.close()
