#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup
from loguru import logger
import user_agents
import json
import os
import time
import pandas as pd
import showman
from threading import Thread
import random

current_page = 0

move_up = '\033[F'
clear_line = '\033[K'
move_down = '\033[B'

logger.remove()

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
def parsing_site(httpx_object, page_tracker):
    try:
        soup = BeautifulSoup(httpx_object.text, 'lxml')
        
        page_tracker += 1

        logger.info(f'Parsing has been successful for URL: {httpx_object.url}')
        logger.info(f'Page number: {page_tracker}')

        return soup

    except Exception as e:
        logger.critical('The parsing of HTML document has been failed... The script will not be able to hold without this function!', e)


def main_page_ingest(bs4_object, website_list):
    item_box = bs4_object.find_all('div', class_='item-box')
    next_page_container = bs4_object.find('li', class_='next-page')
    next_page = next_page_container.find('a')['href']
    
    global current_page
    current_page += 1
    logger.info(f'Product link harvesting has been started for Page {current_page}')

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

    logger.info(f'Product link harvesting has been successfully completed for Page {current_page}')

    return next_page


product_page_iter = 0

product_page_time = None


def product_page_ingest(links_list, save_list):

    while links_list:

        global product_page_iter

        global product_page_time

        start_time = time.perf_counter()

        total_products = len(links_list)

        product_page_time = product_page_iter * total_products

        print(f'On Page: {current_page}')

        print(f'Total items on Page {current_page}: {total_products} products')

        print(f'Time taken per Product: {product_page_iter} seconds')

        print(f'Estimated time for completion: {product_page_time} seconds')

        popped_url = links_list.pop(0)

        print()

        print('Extraction in progess | URL:', popped_url)

        print()

        current_url = popped_url

        # print('Popped_URL:', current_url)
        # print()

        response = session.get(current_url, timeout=25)
        soup = BeautifulSoup(response.text, 'lxml')

        '''with open('product.html', 'w') as f:
            f.write(soup.prettify())'''

        product_container = soup.find_all('div', class_='product-essential')

        for x in product_container:

            capture = {}

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

            size_container = x.find('div', class_='attributes')
            size_ul = size_container.find('ul', class_='option-list button-list') if size_container else None
            sizes = size_ul.find_all('li') if size_ul else []

            image_container = x.find('div', class_='picture-wrapper')
            image = image_container.find('a')['href'] if image_container else 'N/A'

            '''print()
            print('SKU:', sku)
            print('Product Name:', title)
            print('Brand:', brand)
            print('Collection:', collection)
            print('Availability:', availability)
            print('Price:', actual_price)

            for num, item in enumerate(sizes, 1):

                target = item.find('label')

                if 'out-of-stock-variant' in item.get('class', []):
                    print('Size Option: N/A')

                else:
                    print(f'Size {num}: {target.text}')

            table = soup.find('table', class_='data-table')

            if table:
                tr = table.find_all('tr')

                for item in tr:

                    td_name = item.find('td', class_='spec-name')
                    td_info = item.find('td', class_='spec-value')

                    if td_name and td_info:
                        name = td_name.text.strip()
                        info = td_info.text.strip()
                        print(f'{name}: {info}')

            print('Image URL:', image)
            print()'''

            capture['SKU Number'] = sku
            capture['Name'] = title
            capture['Price'] = actual_price
            capture['Brand'] = brand
            capture['Collection'] = collection
            capture['Availablity'] = availability
            capture['Image URL'] = image

            for num, item in enumerate(sizes, 1):

                target = item.find('label')

                if 'out-of-stock-variant' in item.get('class', []):
                    capture[f'Size {num}'] = 'N/A'
                else:
                    capture[f'Size {num}'] = target.text

            table = soup.find('table', class_='data-table')

            if table:
                tr = table.find_all('tr')

                for item in tr:

                    td_name = item.find('td', class_='spec-name')
                    td_info = item.find('td', class_='spec-value')

                    if td_name and td_info:
                        name = td_name.text.strip()
                        info = td_info.text.strip()
                        capture[name] = info

            end_time = time.perf_counter()

            product_page_iter = round(end_time - start_time, 2)

            save_list.append(capture)

            pick = random.uniform(0.1, 0.3)

            showman.carriage_dict(capture, pick)

        print(f'\r{move_up}{clear_line}', end='')

        print(f'\r{move_up}{clear_line}', end='')

        print(f'\r{move_up}{clear_line}', end='')

        print(f'\r{move_up}{clear_line}', end='')

        print(f'\r{move_up}{clear_line}', end='')

        print(f'\r{move_up}{clear_line}', end='')

        print(f'\r{move_up}{clear_line}', end='')

def change_page(url, website_list, save_list, dataframe):

    global current_page

    while url:

        try:
            logger.info('Requesting for the next page...')
            response1 = session.get(url, timeout=25, follow_redirects=True)
            response1.raise_for_status()
            logger.info(f'Request successful! Status Code: {response1.status_code}')

            logger.info(f'Page number: {current_page}')
            logger.info(f'Changing the page to: {response1.url}')

        except httpx.HTTPStatusError as e:
            logger.critical(f'Change page request failed for some reason! | {e.response.url} {e.response.status_code}')

        try:
            soup1 = BeautifulSoup(response1.text, 'lxml')
            logger.info(f'Parsing successful for Page {current_page}')

        except Exception as e:
            logger.error(f'Parsing has failed for some reason! | {e}')

        save_list.clear()
        website_list.clear()

        next_page_url = main_page_ingest(soup1, website_list)
        next_page_ingest = product_page_ingest(website_list, save_list)

        # Ingestion logic

        dataframe.to_csv('Wallpaper_listings.csv', index=False, mode='a', header=False)

        url = next_page_url

        if current_page == 4:

            print(f'\r{move_up}{clear_line}', end='')
            print(f'\r{move_up}{clear_line}', end='')
            showman.carriage_dotprint('Please Wait', True, False)
            showman.carriage_print('Data has been saved into a .csv file!', 0, False, True)
            print()
            print(f'Page Stop is set to {current_page}')
            print('Stopping the script from execution... Our objective is complete!')
            return


if os.path.exists('cookies.json'):  # This if statement is checking if a 'cookies.json' file exists or not

    with open('cookies.json', 'r') as f:    # If that file exists then it will reuse the cookies
        reuse_cookies = json.load(f)
        session.cookies.update(httpx.Cookies(reuse_cookies))

    logger.info('"Cookies.json" file exists! Reloading cookies...\n')
    for x, y in session.cookies.items():
        logger.info(f'{x}: {y}')


product_website = []
collect = []

print('Wallapaper Catalog Ingest | Version 1.10')
print()

showman.carriage_dotprint('Initializing')
time.sleep(1)
print(f'\r{clear_line}', end='')

pr_1 = Thread(target=showman.carriage_dotprint, daemon=True, args=('Script is trying to fetch the website from the server', False, True))

pr_2 = Thread(target=showman.carriage_print, daemon=True, args=('Success! Website has been fetched successfully!', 0, False, True))

time.sleep(2)
pr_1.start()

response = fetch_website(url, 120)

if response:
    pr_2.start()

time.sleep(1.8)
print(f'\r{move_up}{clear_line}', end='')
print(f'\r{move_up}{clear_line}', end='')

browser_cookies()
time.sleep(0.7)
showman.carriage_dotprint('')
time.sleep(1.7)
showman.carriage_print('Cookies grabbed and loaded in!', 2)

print(f'\r{clear_line}', end='')

time.sleep(2)

soup = parsing_site(response, current_page)

showman.carriage_dotprint('Product Link harvesting has been started! Please wait', False, True)

scroll_page = main_page_ingest(soup, product_website)

showman.carriage_print(f'Success! All the links have been harvested from Page {current_page}', 2, False, True)

print()

for x in product_website:
    print(x, flush=True)
    time.sleep(0.03)

time.sleep(2.4)

print(f'\r{move_up}{clear_line}' * len(product_website), end='')

print(f'\r{move_up}{clear_line}', end='')
print(f'\r{move_up}{clear_line}', end='')
print(f'\r{move_up}{clear_line}', end='')

time.sleep(1)

showman.carriage_dotprint('Initiating Crawling from Page to Page also with ingestion, please wait', False, True)
print()

product_page = product_page_ingest(product_website, collect)

data = pd.DataFrame(collect)

data.to_csv('Wallpaper_listings.csv', index=False)
logger.info('Data has also been successfully stored into a .csv file!')

change_page(scroll_page, product_website, collect, data)

session.close()
