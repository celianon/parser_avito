import requests
from bs4 import BeautifulSoup as Bs
import fake_useragent
from time import sleep, time
import random
import csv
from codecs import open
from multiprocessing import Pool
from random import choice


class AvitoMobile:
    base_url = 'https://www.avito.ru/moskva/nedvizhimost?q=%D0%BA%D0%BE%D1%82%D1%82%D0%B5%D0%B4%D0%B6'
    proxy_list_url = 'http://spys.one/proxies/'
    # headers = []
    proxy_list = []
    total_page = None
    url_list = []
    csv_file_path = 'project/data_class.csv'
    total_requests = 0

    def set_sleep(self, a, b, r=False):
        if not r:
            s = random.randint(a, b)
            print(f'Ждем {s} секунд')
            sleep(s)

        elif r:
            s = random.randint(a, b) + random.random()
            print(f'Ждем {s} секунд')
            sleep(s)

    def set_random_sleep(self, a, b, prob, r=False):
        if random.random() < prob:
            self.set_sleep(a, b, r=r)
        else:
            pass

    def get_headers(self):
        self.total_requests += 1
        ua = fake_useragent.UserAgent()
        headers = {'User-Agent': ua.random}
        # self.headers = headers
        return headers

    def set_cookie(self):
        cj = requests.cookies.RequestsCookieJar()

        cj.set('buyer_from_page', 'catalog')
        cj.set('buyer_location_id', '654070')
        cj.set('buyer_selected_search_radius2', '0_job')
        cj.set('dfp_group', '19')
        cj.set('f', '5.25ba337c6fbbd6c1cc0065cb1b69001fe404c9a8ad2fd516e404c9a8ad2fd516e404c9a8ad2fd516e404c9a8ad2fd516d8b16176e03d2873d8b16176e03d2873d8b16176e03d2873e404c9a8ad2fd5160da5ab2fc5c813503d6c212bc3ab3fc346b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fad99271d186dc1cd0e992ad2cc54b8aa8b175a5db148b56e9bcc8809df8ce07f640e3fb81381f359171e7cb57bbcb8e0f2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab868aff1d7654931c9d8e6ff57b051a58973cd7bbe8abaaf87ea66bf55a6037fb938bf52c98d70e5cc074a3cd9c0c8bcd4659aa946bf8012b9154f4aaf0a7b4f4fb0d6023d64b927d84f76fa71ceebba2465d5650ed2fd5c1685428d00dc691fa9e82118971f2ed6494d66450ac1e7292d49cfac105d781bfc772035eab81f5e13de19da9ed218fe2555de5d65c04a913661828fb877cbd03')
        cj.set('rheftjdd', 'rheftjddVal')
        cj.set('sessid', '1614c440eff898569b742cf35ccabba9.1558944442')
        cj.set('sx', 'H4sIAAAAAAACA52RwXLiQAxE / 8XnHGQsb2T + BgRuB8WRjYhlkuLfd6hsUssed25T1fWmX89ndRj9lfQs + pbpbu6hEZSR1fazWqptNb1uYpmM / UVEg5UcoBS9X6TEnqpjta3btqOmburN7anq + qE7Se / NzHCQBUwsOPwbOV5e5npZT7gGKZUDd1iYZ4ilPCKlLsjmvGeZ9uOwA1up50xRHjf + RtZzH + 9v + 6axITXVJN0MFMWGgb + Jm1a6QjxMS15HUm9DoJkajnAp2T / EATGv6 / FjcklmWDoSSU4uRYgfSvIXcoe27 / T9slgJgclYJI30Z8rRbcbu4CeOQBgB7CzOqRJCDy1LzYLsm + cuT + djywRVBCQiyxf8eHfX2i7rvCogMFfcJ1QrK0qC / xH / dUeOFx1ND5aDhllR1qIEw / 8s2cnt9hv05kVfQwIAAA ==')
        cj.set('u', '2fiyx7ia.uge9b5.g3fxtomm4e')
        cj.set('v', '1558944442')

        return cj

    def get_html(self, url, data=None):
        headers = self.get_headers()
        if self.proxy_list:
            proxy = choice(self.proxy_list)
        else:
            proxy = {}

        s = requests.Session()

        cj = self.set_cookie()

        s.cookies = cj
        r = s.get(url, headers=headers, proxies=proxy, data=data)

        return r.text

    def soup(self, content):
        soup = Bs(content, 'lxml')
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
        try:
            try:
                self.set_sleep(0, 5, r=True)
            except:
                print('error 321123')
            # condition = self.check_file(self.csv_file_path, 'more', from_=600, to=700)
            #
            # if condition:
            #     self.set_sleep(30, 50, r=True)
            try:
                r = self.get_html(url)
                soup = self.soup(r)
            except:
                print(f'error {url}')

            try:
                title = soup.find('span', attrs={'class': 'CdyRB _3SYIM _2jvRd'}).text
            except AttributeError:
                title = ''
            try:
                prise = soup.find('span', attrs={'data-marker': 'item-description/price'}).text
            except:
                prise = ''
            try:
                location = soup.find('span', attrs={'data-marker': 'delivery/location'}).text
            except:
                location = ''
            try:
                name = soup.find('span', attrs={'data-marker': 'item-contact-bar/name'}).text
            except:
                name = ''
            try:
                tel = soup.find('a', attrs={'data-marker': 'item-contact-bar/call'}).get('href')[5:]
            except:
                tel = 'нет'

            try:
                print(title, prise, location, name, tel)

                loc_data = {'title': title,
                            'prise': prise,
                            'location': location,
                            'name': name,
                            'tel': tel,
                            'link': url}
            except:
                print(f'error 4 {url}')

            try:
                self.save_csv(loc_data)
            except:
                print('error 2 ')
        except:
            print('error 123')
    def check_file(self, path, condition, from_=0, to=0):
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()

                if condition == 'empty':
                    if not content:
                        return True
                    else:
                        return False

                if condition == 'more':
                    content = content.split('\n')
                    if to > len(content) > from_:
                        return True

        except FileNotFoundError:
            with open(path, 'w'):
                self.check_file(path, condition, from_, to)

    def save_csv(self, loc_data):

        with open(self.csv_file_path, 'a', encoding='utf-8') as file:

            empty = self.check_file(self.csv_file_path, 'empty')
            csv_writer = csv.writer(file)

            if empty:
                head = loc_data.keys()
                csv_writer.writerow(head)

            csv_writer.writerow(loc_data.values())

    def run(self):
        # test
        # base_content = self.get_html(self.base_url)
        #
        # self.pars_link('https://m.avito.ru/moskva/doma_dachi_kottedzhi/kottedzh_181_m_na_uchastke_11_sot._1208728696')

        start = time()

        base_content = self.get_html(self.base_url)
        base_soup = self.soup(base_content)
        self.get_total_pages(base_soup)

        print(f'Всего страниц : {self.total_page}')

        for page in range(self.total_page):
            url = self.base_url.replace('?', f'?p={page}&')
            self.get_link(url)

        self.url_list = list(dict.fromkeys(self.url_list))
        print(f'Количество объявлений : {len(self.url_list)}')

        # self.get_proxy
        try:
            with Pool(50) as p:
                try:
                    p.map(self.pars_link, self.url_list)
                except:
                    print('error 7')
        except:
            print('?')

        end = time()

        print(f'Время выполнения: {(end - start)//60} минут(а/ы) и {round((end - start)%60)} секунд(а/ы)')

if __name__ == '__main__':

    AvitoMobile().run()
