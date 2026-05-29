#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup
from loguru import logger
import user_agents
import json
import os
import time

logger.add('scraper.log', rotation='10 MB')


url = 'https://www.yorkwallcoverings.com/wallpaper-york'

session = httpx.Client(headers=user_agents.brave_linux, http2=True)


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


def main_page_ingest(bs4_object, website_list):
    item_box = bs4_object.find_all('div', class_='item-box')
    print('Number of items in the page:', len(item_box))
    print('\n')
    print('York Wallcoverings Wallpaper Catalog Showcase:')
    print()

    for x in item_box:
        title_container = x.find('h3', class_='product-title')
        title = title_container.find('a').text
        price_container = x.find('div', class_='prices')
        price = price_container.find('span', class_='price actual-price avoid-wrap').text
        actual_price = price.strip('Actual Price:USD ')

        product_container = x.find('div', class_='picture')
        product_link = product_container.find('a')['href']

        product_sku_number = product_container.find('a')['onclick']

        strip_product_prefix = product_sku_number.removeprefix('productClick("')
        strip_product_suffix = strip_product_prefix.removesuffix(')"')
        strip_product = strip_product_suffix.strip()
        split_product = strip_product.split(',')
        sku_number = split_product[1]
        sku_number_cleaned = sku_number.removesuffix('SAM')
        sku_number_final = sku_number_cleaned.upper()

        base_url = 'https://www.yorkwallcoverings.com'

        '''print('Name:', title)
        print('Price:', actual_price)
        print('Link:', base_url + product_link)
        # print('SKU Info:', product_sku_number)
        # print('Cleaned SKU Info:', strip_product)
        # print('Scram SKU Info:', split_product)
        print('Extracted SKU Number:', sku_number_final)
        print()'''
        
        website_list.append(base_url + product_link + '/' + sku_number_final)


def product_page_ingest(links_list):

    while links_list:

        popped_url = links_list.pop(0)
        current_url = popped_url
        print('Popped_URL:', current_url)
        print()
        response = session.get(current_url, timeout=25)
        soup = BeautifulSoup(response.text, 'lxml')
        with open('product.html', 'w') as f:
            f.write(soup.prettify())
            print('The soup document has been saved into an HTML file')

        product_container = soup.find_all('div', class_='product-essential')

        for x in product_container:

            title = x.find('div', class_='product-name').text

            brand_container = x.find('div', class_='manufacturers')
            brand = brand_container.find('span', itemprop='brand').text

            availability_container = x.find('div', class_='availability')
            availability = availability_container.find('span', class_='value').text if availability_container else 'N/A'

            sku_container = x.find('div', class_='sku')
            sku = sku_container.find('span', class_='value').text if sku_container else 'N/A'

            collection_container = x.find('div', class_='collection')
            collection = collection_container.find('a').text if collection_container else 'N/A'

            price_container = x.find('div', class_='prices')
            price = price_container.find('span', class_='label') if price_container else 'N/A'
            price_main = price.find_next_sibling().text if price_container else 'N/A'
            actual_price = price_main.removeprefix(' USD ').strip() if price_container else 'N/A'

            print()
            print('SKU:', sku)
            print('Product Name:', title)
            print('Brand:', brand)
            print('Collection:', collection)
            print('Availability:', availability)
            print('Price:', actual_price)
            print()



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
time.sleep(3)
browser_cookies()
soup = parsing_site(response)
time.sleep(2)
wallpaper = main_page_ingest(soup, product_website)
print()

product_info = product_page_ingest(product_website)


session.close()
