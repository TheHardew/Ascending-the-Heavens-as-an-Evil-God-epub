#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sys
import re
import os

if len(sys.argv) != 2:
    print("Please provide a command line argument!")
    exit()

# URL of the webpage
url = sys.argv[1]
match = re.search(r'/(chapter-\d+)', url).group(1)
match = f'chapters/{match}'

if os.path.exists(match):
    exit()

try:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        target_article = soup.find('article', class_='blog-post-page-font')
        if target_article:
            content = str(target_article)

            with open(match, 'w', encoding='utf-8') as file:
                file.write(content)
                print(match)
        else:
            print("Article not found on the webpage.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
