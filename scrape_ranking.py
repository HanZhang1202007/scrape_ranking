import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.usnews.com/education/best-global-universities/search?name=Harvard+University'
# URL = 'https://www.usnews.com/education/best-global-universities/rankings'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
}

def get_universities(path):
    df = pd.read_excel(path)
    universities = df['PI1_inst_name']
    return universities

def fetch_university_details(url):
    print('getting response')
    response = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    universities = []
    # print(response.text)
    for card in soup.find_all('div', class_='DetailCardGlobalUniversities__CardOverview-sc-1v60hm5-4'):
        name_tag = card.find('h2', class_='Heading-sc-1w5xk2o-0').find('a')
        name = name_tag.text.strip()
        
        location_tag = card.find('p', class_='Paragraph-sc-1iyax29-0')
        country = location_tag.find('span', style="font-weight:700").text.strip()
        city = location_tag.find_all('span')[-1].text.strip()
        
        rank_tag = card.find('div', class_='RankList__Rank-sc-2xewen-2')
        rank = rank_tag.text.strip('#').strip()
        
        universities.append({
            'name': name,
            'country': country,
            'city': city,
            'rank': rank
        })
    
    return universities

if __name__ == "__main__":
    path = './analysis/uct.xlsx'
    universities = get_universities(path)
    for uni in universities:
        URL = 'https://www.usnews.com/education/best-global-universities/search?name='
        university_details = fetch_university_details(URL)
        for university in university_details:
            print(f"Name: {university['name']}, Country: {university['country']}, City: {university['city']}, Rank: {university['rank']}")
