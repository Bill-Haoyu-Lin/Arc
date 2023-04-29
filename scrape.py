import io
import csv
import datetime
import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
    }

day = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '日': 7,
}

def get_curr_season():
    now = datetime.datetime.now()
    curr_year = str(now.year)
    curr_month = now.month

    # 一/四/七/十月新番
    if curr_month >= 1 and curr_month <= 3:
        curr_season = curr_year + '01'
    elif curr_month >= 4 and curr_month <= 6:
        curr_season = curr_year + '04'
    elif curr_month >= 7 and curr_month <= 9:
        curr_season = curr_year + '07'
    elif curr_month >= 10 and curr_month <= 12:
        curr_season = curr_year + '10'
    
    return curr_season


def main():
    url = 'https://acgsecrets.hk/bangumi/{}/'.format(get_curr_season())
    
    page_text = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(page_text, 'html.parser')
    content = soup.find('div', {'id':'acgs-anime-icons'})
    animes = content.find_all('div', recursive=False)
    anime_list = []

    for anime in animes:
        name = anime.find('div', {'class':'anime_name'}).text
        date = day[anime.find('div', {'class':'day'}).text]
        time = anime.find('div', {'class':'time'}).text
        img = anime.find('img', {'class':'img-fit-cover'})['src']
        anime_list.append([name, date, time, img])

    return anime_list
    
    
    
if __name__ == '__main__':
    main()