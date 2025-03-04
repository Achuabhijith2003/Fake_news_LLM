import requests
from bs4 import BeautifulSoup 
import Config.config as config
from urllib.parse import urljoin

# url=' '

# Collect the data of the web {Heading & Articals}
def webscrap(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    paragraphs = soup.find_all('p')
    with open(config.news, 'a', encoding='utf-8') as file:
        file.write(soup.title.string + '\n')
        print("Processing this url: ", url)
        for para in paragraphs:
            
            file.write(para.text + '\n')

    pass
# Collect the links from the website
def get_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for link in soup.find_all('a', href=True):  # Corrected 'herf' to 'href'
        full_link = urljoin(url, link['href'])
        if checklink(full_link):
            webscrap(full_link)
        else:
            continue
    
# check we don't go from outside the domain
def checklink(url):
    if url.startswith('https://www.thehindu.com') or url.startswith('http://www.thehindu.com'):
        return True
    else:
        return False
    