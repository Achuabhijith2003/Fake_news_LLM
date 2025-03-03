import requests
from bs4 import BeautifulSoup 
import Config.config as config

def webscrap():
    r = requests.get('https://www.thehindu.com/news/national/telangana/telangana-slbc-tunnel-collapse-rescue-day-10-live-march-3-2025/article69284070.ece')


    soup = BeautifulSoup(r.content, 'html.parser')


    print("Title of the page is: ", soup.title.string)
    paragraphs = soup.find_all('p')
    with open(config.news, 'w', encoding='utf-8') as file:
        file.write(soup.title.string + '\n')
        for para in paragraphs:
            file.write(para.text + '\n')
        
        

    pass 