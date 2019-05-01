from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
from random import choice
from codecs import open
import xlwt
import xlrd
import os
from xlutils.copy import copy


headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 '
                          '(KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.9'}
           ]
proxy = [{
        'https': 'https://84.201.254.47:3128'
    },
    {
        'https': 'https://217.113.122.142:3128'
    },
    {
        'https': 'https://91.208.39.70:8080'
    },
    {
        'https': 'https://37.79.244.120:3128'
    },
    {
        'https': 'https://91.208.39.70:8080'
    }
]

list_ = []
list_link = []
data = []


def get_html(url):
    for i in range(100):
        if len(proxy) == 0:
            print('Прокси закончились')
            exit(1)
        else:
            random_proxy = choice(proxy)
            try:
                random_headers = choice(headers)
                r = requests.get(url, headers=random_headers, proxies=random_proxy)
                if 'вашего IP-адреса временно ограничен' in r.text:
                    print(f'Прокси {random_proxy["https"]} заблокирована')
                    proxy.remove(random_proxy)
                    continue
                return r.text
            except:
                proxy.remove(random_proxy)
                print(f'Прокси {random_proxy["https"]} не работает')
                continue
    exit(1)


def get_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_pages(soup):
    try:
        pages = soup.find('div', class_='pagination-pages clearfix')
        page = pages.findAll('a', class_='pagination-page')[-1].get('href').split('?p=')[1].split('&q=')[0]
        return int(page)
    except:
        print('Не удалось получить количество станиц')
        exit(1)


def clean(path):
    with open(path, 'w') as f:
        f.write('')


def get_pages_urls(url, page):
    for i in range(page):
        first = url.split('?p=1')[0]
        second = url.split('?p=1')[1]
        a = f'{first}?p={i + 1}{second}'
        list_.append(a)
    return list_


def pars_url(url):
    url = f'https://{url}'

    try:
        soup = get_soup(get_html(url))

        title = soup.find('span', class_='title-info-title-text').text
        square = title.split('м²,')[0].split(',')[1].strip() + ' м²'
        floor = title.split('м², ')[1]
        description = soup.find('div', itemprop='description').text.lower()
        status = check_status(description)

        if status == 'Продается':
            prise = soup.find('span', class_='js-item-price').text + ' рублей'
        else:
            prise1 = soup.find('span', class_='js-item-price').text
            prise2 = soup.find('span', class_='price-value-string js-price-value-string').contents[-1]
            prise = f'{prise1} рублей {prise2}'

        address = soup.find('div', class_='item-view-contacts js-item-view-contacts') \
            .findAll('div', class_='seller-info-value')[-1].text.strip()

        name = soup.find('div', class_='item-view-contacts js-item-view-contacts') \
            .findAll('div', class_='seller-info-value')[-2].text.strip()

        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 0
        font0.bold = True

        style0 = xlwt.XFStyle()
        style0.font = font0

        if not os.path.isfile('data.xls'):
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Avito', cell_overwrite_ok=True)
            wb.save('data.xls')
            ws.col(0).width = 3000
            ws.col(1).width = 4285
            ws.col(2).width = 3400
            ws.col(3).width = 5500
            ws.col(4).width = 5500
            ws.write(0, 0, 'Площадь', style0)
            ws.write(0, 1, 'Этаж / из скольки', style0)
            ws.write(0, 2, 'Статус', style0)
            ws.write(0, 3, 'Цена', style0)
            ws.write(0, 4, 'Адресс', style0)
            ws.write(0, 5, 'Имя', style0)
            ws.write(0, 6, 'Ссылка', style0)

            length = 1

        else:
            book = xlrd.open_workbook('data.xls')
            sheet = book.sheet_by_index(0)
            length = len(sheet.col(0))
            wb = copy(book)
            ws = wb.get_sheet(0)
            ws.col(0).width = 3000
            ws.col(1).width = 4285
            ws.col(2).width = 3400
            ws.col(3).width = 5500
            ws.col(4).width = 5500

        ws.write(length, 0, square, )
        ws.write(length, 1, floor)
        ws.write(length, 2, status)
        ws.write(length, 3, prise)
        ws.write(length, 4, address)
        ws.write(length, 5, name)

        link = f'HYPERLINK("{url}"; "{url}")'
        ws.write(length, 6, xlwt.Formula(link))

        wb.save('data.xls')

        print(f'Получены данные о {title}')

    except:
        print(f'Что-то пошло не так на {url}')


def get_link(page):
    soup = get_soup(get_html(page))
    item = soup.findAll('div', class_='item_table-wrapper')
    for i in item:
        link = i.find('a', class_='item-description-title-link').get('href')
        link = 'avito.ru' + link
        list_link.append(link)

    with open('links.txt', 'a') as file:
        for i in list_link:
            file.write(f'{i}\n')


def check_status(desc):
    status = 'неизвестно'
    sell = 'прода'
    rent = 'сда'
    if sell in desc:
        status = 'Продается'
    if rent in desc:
        status = 'Сдается'
    return status


if __name__ == '__main__':
    # url = 'https://www.avito.ru/ekaterinburg/kvartiry?p=1&q=1%20%D0%BA%D0%BE%D0%BC%D0%BD%D0%B0%D1%82%D0%BD%D0%B0%D1%8F'
    #
    # clean('links.txt')
    #
    # print('Получение количества страниц...')
    #
    # page = get_pages(get_soup(get_html(url)))
    #
    # print(f'Страниц всего {page}')
    #
    # list_ = get_pages_urls(url, page)
    #
    # print('Получение ссылок на товар...')
    #
    # with Pool(30) as p:
    #     p.map(get_link, list_)
    #
    # print('Сбор данных...')
    #
    # with open('links.txt', 'r') as f:
    #     list_link = f.read().split('\n')
    #
    # print(f'Всего {len(list_link)}')
    #
    # with Pool(40) as p:
    #     p.map(pars_url, list_link)
    pars_url('avito.ru/ekaterinburg/kvartiry/1-k_kvartira_53_m_725_et._1027214735')
