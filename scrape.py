import re
import pytz
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
now = datetime.datetime.now().replace(second=0, microsecond=0)
curr_year = str(now.year)
curr_month = now.month

# Spring, summer, fall, winter season
def get_curr_season(eng = False):
    if curr_month >= 1 and curr_month <= 3:
        curr_season = (curr_year + '/winter') if eng else (curr_year + '01')
    elif curr_month >= 4 and curr_month <= 6:
        curr_season = (curr_year + '/spring') if eng else (curr_year + '04')
    elif curr_month >= 7 and curr_month <= 9:
        curr_season = (curr_year + '/summer') if eng else (curr_year + '07')
    elif curr_month >= 10 and curr_month <= 12:
        curr_season = (curr_year + '/fall') if eng else (curr_year + '10')
    
    return curr_season

# Convert anime start day & time from China Standard Time to local time zone
def to_local_time(day, time, zone = 'cst'):
    tz = pytz.timezone('Asia/Shanghai') if zone == 'cst' else pytz.timezone('Asia/Tokyo')
    web_time = datetime.datetime.now(tz).replace(second=0, microsecond=0, tzinfo=None)
    time_diff = int((now - web_time).total_seconds() / 3600)
    hour = int(time[:2]) + time_diff
    
    if hour < 0:
        hour = 24 + hour
        time = '0' + str(hour) + time[2:] if hour < 10 else str(hour) + time[2:]
        if day != 0:
            day -= 1
        else:
            day = 6
    else:
        time = '0' + str(hour) + time[2:] if hour < 10 else str(hour) + time[2:]
        
    return day, time

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

            day, time = to_local_time(day, time)
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
        
        day, time = to_local_time(day, time)
        anime_list.append([name, day, time, img])

    return anime_list

# Helper function for anime_eng()
# Get weekday and time for specific anime on myanimelist.net
def get_date_time(url):
    page_text = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(page_text, 'html.parser')
    content = soup.find('span', string=re.compile('Broadcast:')).next_sibling.strip().split()
    
    day = weekday[content[0][:-1]]
    time = content[2]
    zone = content[3][1:-1]
    
    return to_local_time(day, time, zone)

def anime_eng():
    anime_list = []
    url = 'https://myanimelist.net/anime/season/{}'.format(get_curr_season(True))
    page_text = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(page_text, 'html.parser')
    content = soup.find('div', {'class':'seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1'})
    animes = content.find_all('div', {'class':'js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-1'})
    
    for anime in animes:
        name = anime.find('span', {'class':'js-title'}).text
        link = anime.find('a')['href']
        day, time = get_date_time(link)
        img_tag = anime.find('img')
        img = img_tag.get('src') or img_tag.get('data-src')
        
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
        anime_list = anime_eng()
    
    anime_list = sorted(anime_list, key=sort_key)
    # for anime in anime_list:
    #     print(anime)
    return anime_list