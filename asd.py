import requests
import csv
from bs4 import BeautifulSoup
import datetime

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def get_urls():
    i = 0
    request = requests.session()
    while True:
        day = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y/%m/%d')
        i += 1
        url_date = 'https://pravdasevera.ru/' + day + '/'

        request.get(url_date)
        query_date = request.get(url=url_date)
        bs = BeautifulSoup(query_date.text, 'lxml')

        url_list = []

        find_url = bs.findAll('a', class_='nitem')

        for url_of_news in find_url:
            href = url_of_news.get('href')
            url_list.append(href)

        if day == '2016/12/31':
            break

        with open('url_list.txt', 'a') as liink:
            for link in url_list:
                if link[-1] == "l":
                    liink.write(f'https://pravdasevera.ru{link}\n')


def parse():
    # get_urls()

    with open('url_list.txt') as file:
        url_list = [line.strip() for line in file.readlines()]

    request = requests.Session()
    result_data = []
    for url in url_list:
        try:
            query = request.get(url=url)
            bs = BeautifulSoup(query.text, 'lxml')

            title_news = bs.find('body').find('h1').get_text(strip=True)
            summary_news = bs.find('body').find('div', class_='summary').get_text(strip=True)
            text_news = bs.find('div', class_='block--article__text').get_text(strip=True)
            tag_news = bs.find('div', class_='tags').find('a').get_text(strip=True)

            result_data.append(
                {'url': url, 'title': title_news, 'summary': summary_news, 'text': text_news, 'tag': tag_news, })

            with open('result.csv', "w", encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['url', 'title', 'summary', 'text', 'tag'])
                for element in result_data:
                    writer.writerow(
                        [element['url'], element['title'], element['summary'], element['text'], element['tag']])
        except:
            continue


def main():
    parse()


if __name__ == '__main__':
    main()