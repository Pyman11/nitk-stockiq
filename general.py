
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_general():
    url = 'https://finance.yahoo.com/topic/stock-market-news'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('li', class_='js-stream-content')

    news_data = []
    news_links = []

    for article in articles:
        try:
            title = article.find('h3').text
            link = article.find('a')['href']
            summary = article.find('p').text if article.find('p') else 'No summary available'
            
            news_data.append( "• " + title )
            news_links.append ( f'{link}' )
            news_data.append( "" )
            news_links.append ( "" )
        except AttributeError:
            continue

    return [ news_data, news_links ]
