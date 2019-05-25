import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
from time import sleep
import random
import csv
from codecs import open
from multiprocessing import Pool
from random import choice
from pprint import pprint


class AvitoMobile:
    base_url = 'https://www.avito.ru/moskva/nedvizhimost?q=%D0%BA%D0%BE%D1%82%D1%82%D0%B5%D0%B4%D0%B6'
    proxy_list_url = 'http://spys.one/proxies/'
    headers = []
    proxy_list = []
    total_page = None
    url_list = []
    csv_file_path = 'project/data_class.csv'
    total_requests = 0

    def set_sleep(self, a, b, r=False):
        if not r:
            sleep(random.randint(a, b))

        elif r:
            sleep(random.randint(a, b) + random.random())

    def set_random_sleep(self, a, b, prob, r=False):
        if random.random() < prob:
            if not r:
                sleep(random.randint(a, b))

            elif r:
                sleep(random.randint(a, b) + random.random())
        else:
            pass

    def get_headers(self):
        self.total_requests += 1
        ua = fake_useragent.UserAgent()
        headers = {'User-Agent': ua.random}
        self.headers = headers

    def get_html(self, url, data=None):
        self.get_headers()
        if self.proxy_list:
            proxy = choice(self.proxy_list)
        else:
            proxy = {}
        r = requests.get(url, headers=self.headers, proxies=proxy, data=data)
        return r.text

    def soup(self, content):
        soup = bs(content, 'lxml')
        return soup

    def get_proxy(self):
        self.proxy_list = []

    def get_total_pages(self, soup):
        total_page = soup.find('div', class_='pagination-pages clearfix')\
                    .find_all('a')[-1].get('href').split('?p=')[1].split('&')[0]
        self.total_page = int(total_page)

    def get_link(self, url):
        self.set_random_sleep(2, 4, 0.6, r=True)
        r = self.get_html(url)
        soup = self.soup(r)
        items = soup.find_all('div', class_='item')
        for item in items:

            a = item.find('a', class_='item-description-title-link')
            if a is None:
                a = item.find('a', class_='description-title-link')
            href = a.get('href')

            url = 'https://m.avito.ru' + href
            print(f'{len(self.url_list)}. {url}')
            self.url_list.append(url)

    def pars_link(self, url):
        self.set_sleep(3, 6, r=True)

        r = self.get_html(url)

        soup = self.soup(r)
        try:
            title = soup.find('span', attrs={'class': 'CdyRB _3SYIM _2jvRd'}).text
        except AttributeError:
            title = ''
        prise = soup.find('span', attrs={'data-marker': 'item-description/price'}).text
        location = soup.find('span', attrs={'data-marker': 'delivery/location'}).text
        name = soup.find('span', attrs={'data-marker': 'item-contact-bar/name'}).text
        try:
            tel = soup.find('a', attrs={'data-marker': 'item-contact-bar/call'}).get('href')[5:]
        except:
            tel = 'нет'

        print(title, prise, location, name, tel)

        loc_data = {'title': title,
                    'prise': prise,
                    'location': location,
                    'name': name,
                    'tel': tel,
                    'link': url}

        self.save_csv(loc_data)

    def save_csv(self, loc_data):

        with open(self.csv_file_path, 'a', encoding='utf-8') as file:

            with open(self.csv_file_path, encoding='utf-8') as f:
                content = f.read()
                if not content:
                    empty = True
                else:
                    empty = False

            csv_writer = csv.writer(file)

            if empty:
                head = loc_data.keys()
                csv_writer.writerow(head)

            csv_writer.writerow(loc_data.values())

    def run(self):

        base_content = self.get_html(self.base_url)
        base_soup = self.soup(base_content)
        self.get_total_pages(base_soup)

        print(f'Всего страниц : {self.total_page}')

        for page in range(self.total_page):
            url = self.base_url.replace('?', f'?p={page}&')
            self.get_link(url)

        self.url_list = list(dict.fromkeys(self.url_list))
        print(f'Количество объявлений : {len(self.url_list)}')

        # self.get_proxy()
        print(self.proxy_list)
        try:
            with Pool(30) as p:
                p.map(self.pars_link, self.url_list)
        except:
            print(1)


if __name__ == '__main__':

    AvitoMobile().run()

# todo save data on excel table
# todo get all link ~916 instead ~900 now (self.url_list = list( dict.fromkeys(self.url_list) ) - remove copy ? )
# todo don't rewrite data
