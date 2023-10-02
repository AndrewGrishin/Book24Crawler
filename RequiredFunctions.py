# Required to be installed
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
# Pre-installed
import json
import re
import sys
import platform
import os
from time import sleep

# Get Requests.response object
def get_resp(url, params=None):
    ua = UserAgent()
    if params is None:
        params = dict()
    headers = {'User-Agent': ua.random}
    resp = requests.get(url, params=params, headers=headers)
    return resp

# Get bs4 object to the passed url
def get_soup(url, params=None):
    resp = get_resp(url, params=params)
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup

# Gather all links to books from webpage
def get_books_links_from_page(soup, scheme):
    links = soup.select('div.product-card__image-holder > a')
    links = list(map(lambda link: scheme + link['href'], links))
    return links

# Gather all info about one book from its page
def get_single_book_data(soup, url, scheme):
    data = dict()

    # selectors for gathering required data
    selectors = {
        'classification': 'ol[itemscope=itemscope] span[itemprop=name]',
        'description': 'div#product-characteristic > dl.product-characteristic__list',
        'abstract': 'div.product-about.product-detail-page__product-about > div.product-about__text',
        'side_bar': 'div.product-sidebar.product-detail-page__sidebar',
        'vendor_code': 'p.product-detail-page__article',
        'rating': 'div.product-ratings-widget',   
    }
    
    # get classification block of book
    classification = soup.select(selectors['classification'])
    data['Классификация'] = []
    try:
        classification = list(map(lambda x: x.text.strip(), classification[1:]))
        title = classification[-1]
        data['Название'] = title
        data['Классификация'] = classification[:-1]
    except:
        pass

    # get description block
    description = soup.select_one(selectors['description'])
    try:
        characteristics = description.find_all('div')

        for element in characteristics:
            key = element.select_one('dt.product-characteristic__label-holder')
            key = key.get_text().replace(':', '').strip()

            value = element.select_one('dd.product-characteristic__value')
            value = value.get_text().strip()

            data[key] = value

        page_links = [url, *map(lambda x: scheme + x['href'], description.select('a'))]
        data['URL'] = page_links
    except:
        pass
    
    # get abstract
    abstract = soup.select(selectors['abstract'])
    data['Описание'] = '-'
    try:
        for element in abstract:
            data['Описание'] += element.get_text()
    except:
        pass

    # get the price block
    side_bar = soup.select_one(selectors['side_bar'])
    availability = '-'
    price = '-'

    try:
        availability = side_bar.select_one('div').get_text().strip()
    except:
        pass

    try:
        price = side_bar.select_one('div[itemprop=offers] > span.app-price.product-sidebar-price__price')
        price = price.get_text().strip().split()[0]
    except:
        pass

    # get the vendor block
    vendor_code = soup.select_one(selectors['vendor_code']).text.strip().split()[-1]

    # get rating (local, NOT livelib)
    rating = soup.select_one(selectors['rating'])
    main_text = '0'
    additional_text = '0'
    try:
        main_text = rating.select_one('span.rating-widget__main-text').text.strip()
    except:
        pass
    
    try:
        additional_text = rating.select_one('span.rating-widget__other-text').text.strip()
    except:
        pass

    data['Наличие товара'] = availability
    data['Цена'] = price
    data['Артикул'] = vendor_code
    data['Оценка'] = main_text.replace(',','.')
    data['Количество оценок'] = additional_text.replace(')', '').replace('(','')
        
    return data

# Get number of pages
def get_number_of_pages(search_url, params):
    soup = get_soup(search_url, params=params)
    search_description = soup.select_one('div.search-page__desc').text
    pattern = re.compile(r'[0-9]+')
    all_books = int(re.search(pattern, search_description).group(0))

    books_per_page = 30
    total_pages = all_books // books_per_page + int(all_books % books_per_page != 0)

    return total_pages

# Cear screen
def clear_screen():
    if 'windows' in platform.system().lower():
        os.system('cls')
    else:
        os.system('clear')

# Gat all data according to requests
def get_data(search_url, params, scheme, file_name):
    gathered_data = []

    total_pages = get_number_of_pages(search_url, params)
    page_pbar = tqdm(range(1, total_pages + 1), desc='Page', disable=True)

    for page_number in page_pbar:
        search_url = f'https://book24.ru/search/page-{page_number}/'
        soup = get_soup(search_url, params=params)
        book_links = get_books_links_from_page(soup, scheme)

        book_pbar = tqdm(
            book_links, 
            desc=f'Page: {page_number}/{total_pages}. Book', 
            disable=False, 
            ncols=70
        )
        for book_link in book_pbar:
            book_soup = get_soup(book_link)
            gathered_data.append(get_single_book_data(book_soup, book_link, scheme))
            sleep(0.5)
        
        sleep(1)

    with open(f'{file_name}', 'w', encoding='utf-8') as f:
        json.dump(gathered_data, f, indent=4, ensure_ascii=False)
    print(f'\nSuccess: {file_name} created!')
    print(f'Gathered {len(gathered_data)} books.')
