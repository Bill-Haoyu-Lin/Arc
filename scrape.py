import datetime
import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
    }

weekday = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7,
}

now = datetime.datetime.now()
curr_year = str(now.year)
curr_month = now.month
    
def get_curr_season():

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
    url = 'https://yuc.wiki/{}/'.format(get_curr_season())
    print(url)
    page_text = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(page_text, 'html.parser')
    animes = soup.find_all('div', {'style':'float:left'})
    
    
    for anime in animes:
        try:
            name = anime.find('td', {'class':'date_title'}).text
            date = anime.find('p', {'class':'imgtext'}).text[:-1] + '/' + curr_year
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
            day = weekday[date.strftime("%A")]
            time = anime.find('p', {'class':'imgep'}).text[:-1]
            img = anime.find('img')['src']
            print(name)
            print(day)
            print(time)
            print(img)
            print()
        except:
            pass  
    
    
if __name__ == '__main__':
    main()