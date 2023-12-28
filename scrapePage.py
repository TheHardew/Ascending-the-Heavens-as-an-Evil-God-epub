#!/bin/python

import requests
from bs4 import BeautifulSoup
import sys
import re

if len(sys.argv) != 2:
    print("Nya~! Please provide a command line argument! (>_<)")
    exit()

# URL of the webpage
url = sys.argv[1]
match = re.search(r'/(chapter-\d+)', url).group(1)
try:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        target_article = soup.find('article', class_='blog-post-page-font')
        if target_article:
            content = str(target_article)

            with open(f'scraped/{match}', 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            print("Div not found on the webpage.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
