from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from abc import ABCMeta, abstractstaticmethod


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/news', methods=['GET'])
class SiteScraper(metaclass=ABCMeta):
    @abstractstaticmethod
    def articles():
        """Создание абстрактного метода"""


def get_all_news():
    tut_by = ScraperFactory.get_scraper('TUTScraper')
    tut_by_articles = tut_by.get_articles()
    cnn_com = ScraperFactory.get_scraper('CNNScraper')
    cnn_com_articles = cnn_com.get_articles()
    factory_news = tut_by_articles + cnn_com_articles
    return jsonify({'news': factory_news})


@app.route('/news/tut.by', methods=['GET'])
class TUTScraper(SiteScraper):
    def __init__(self):
        self.name = 'tut.by'
        self.url = 'https://www.tut.by'

    def articles(self):
        bs = html(self.url)
        tut_news = bs.find('div', id='latest').find_all('a', class_='entry__link io-block-link')
        news_tut_by = []
        for news in tut_news:
            link_tut = news.get('href')
            article_tut = html(link_tut)
            header_tut = ' '.join(article_tut.find('div', {'class': 'b-article'}).find('h1').text.split())
            text_tut = ' '.join(article_tut.find('div', attrs={'id': 'article_body'}).text.split())

            news_tut_by.append({'name': self.name,
                                'link': link_tut,
                                'header': header_tut,
                                'text': text_tut,
                                })
        return news_tut_by


def get_tutby_news():
    tut_by = ScraperFactory.get_scraper('TUTScraper')
    tutby_articles = tut_by.get_articles()
    return jsonify({'news': tutby_articles})


@app.route('/news/cnn.com', methods=['GET'])
class CNNScraper(SiteScraper):
    def __init__(self):
        self.name = 'cnn.com'
        self.url = 'https://edition.cnn.com/world'

    def articles(self):
        bs = html(self.url)
        cnn_news = bs.find('div', id='latest').find_all('span', class_='cd__headline-text')
        news_cnn_com = []
        for news in cnn_news:
            link_cnn = news.get('href')
            article_cnn = html(link_cnn)
            header_cnn = ' '.join(article_cnn.find('div', {'class': 'cd__content'}).find('h3').text.split())
            text_cnn = ' '.join(article_cnn.find('div', attrs={'class': 'pg-rail-tall__body'}).text.split())

            news_cnn_com_by.append({'name': self.name,
                                    'link': link_cnn,
                                    'header': header_cnn,
                                    'text': text_cnn,
                                    })
        return news_cnn_com


def get_cnn_news():
    cnn_com = ScraperFactory.get_scraper('CNNScraper')
    cnncom_articles = cnn_com.get_articles()
    return jsonify({'news': cnncom_articles})


class ScraperFactory():
    @staticmethod
    def scraper(news):
        try:
            if news == 'TUTScraper':
                return TUTScraper()
            if news == 'CNNScraper':
                return CNNScraper()
            raise AssertionError('Scraper is not defined')
        except AssertionError:
            print('AssertionError')


def html(url):
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    session = requests.Session()
    r = session.get(url, headers=headers)
    return BeautifulSoup(r.text, 'lxml')


if __name__ == '__main__':
    app.run(debug=True)