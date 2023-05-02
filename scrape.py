import re
import datetime
import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
    }

weekday = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
    
    '一': 0,
    '二': 1,
    '三': 2,
    '四': 3,
    '五': 4,
    '六': 5,
    '日': 6
}

# Get current month and year
now = datetime.datetime.now()
curr_year = str(now.year)
curr_month = now.month

# Spring, summer, fall, winter season
def get_curr_season():
    if curr_month >= 1 and curr_month <= 3:
        curr_season = curr_year + '01'
    elif curr_month >= 4 and curr_month <= 6:
        curr_season = curr_year + '04'
    elif curr_month >= 7 and curr_month <= 9:
        curr_season = curr_year + '07'
    elif curr_month >= 10 and curr_month <= 12:
        curr_season = curr_year + '10'
    
    return curr_season

# Source: yuc.wiki, language: Chinese Simplified
def anime_chs():
    anime_list = []
    url = 'https://yuc.wiki/{}/'.format(get_curr_season())
    page_text = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(page_text, 'html.parser')
    animes = soup.find_all('div', {'style':'float:left'})
    
    for anime in animes:
        try:
            name = anime.find('td', class_=re.compile('^date_title.*')).text
            date = anime.find('p', {'class':'imgtext'}).text.split('~')[0] + '/' + curr_year
            time = anime.find('p', {'class':'imgep'}).text.split('~')[0]
            img = anime.find('img')['src']
            
            # Change date to weekday
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
            day = weekday[date.strftime("%A")]
            
            # Move time >= 24:00 to the next day
            if int(time[:2]) >= 24:
                time = '0' + str(int(time[:2]) - 24) + time[2:]
                if day != 6:
                    day += 1
                else:
                    day = 0

            anime_list.append([name, day, time, img])
        except:
            pass 
    
    return anime_list

# Source: acgsecrets.hk, language: Chinese Traditional
def anime_cht():
    anime_list = []
    url = 'https://acgsecrets.hk/bangumi/{}/'.format(get_curr_season())
    page_text = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(page_text, 'html.parser')
    content = soup.find('div', {'id':'acgs-anime-icons'})
    animes = content.find_all('div', recursive=False)
    
    for anime in animes:
        name = anime.find('div', {'class':'anime_name'}).text
        day = weekday[anime.find('div', {'class':'day'}).text]
        time = anime.find('div', {'class':'time'}).text
        img = anime.find('img', {'class':'img-fit-cover'})['src']
        
        anime_list.append([name, day, time, img])

    return anime_list

# Sort anime list based on weekday and time
def sort_key(anime_list):
    time = datetime.datetime.strptime(anime_list[2], '%H:%M')
    
    return (anime_list[1], time)

# Get anime list based on desired language
def get_anime(lang = 'chs'):
    if lang == 'chs':
        anime_list = anime_chs()
    elif lang == 'cht':
        anime_list = anime_cht()
    elif lang == 'eng':
        anime_list = []
    
    anime_list = sorted(anime_list, key=sort_key)
    # for anime in anime_list:
    #     print(anime)
    return anime_list