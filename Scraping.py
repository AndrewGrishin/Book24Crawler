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
# Imported from other files
from RequiredFunctions import *

if __name__ == '__main__':
    query = " ".join(sys.argv[1:])
    
    initial_query = query.lower()
    out_put_query_name = query.replace(' ', '_')
    # urls and params for requests
    search_url = 'https://book24.ru/search/page-1/'
    scheme = 'https://book24.ru'
    params = {'q': initial_query}

    # Form the name of the output json
    file_name = f'{out_put_query_name}.json'

    # Gather all data according to the initial query
    get_data(search_url, params, scheme, file_name)