import requests
from read_config import proxy as path
from read_config import headers
from random import choice
import sys


with open(path) as p:
	proxy_list = p.read().split('\n')
	for i, data in enumerate(proxy_list):
		proxy_list[i] = data.replace('\t', ':')


def check_proxy(proxy_list):
	global proxy
	proxy = choice(proxy_list)

	try:
		r = requests.get('http://sitespy.ru/my-ip',headers=headers , proxies={'http' : f'http://{proxy}'}, timeout=3)
		if r.status_code == 200:
			print(f'Использованная прокси : {proxy}')
			

	except:
		print(f'Не удалось подключиться с {proxy}')
		proxy_list.remove(proxy)

		if proxy_list == []:
			print('Прокси закончились ')
			sys.exit(0)
		check_proxy(proxy_list)
	finally:
		return proxy

proxy = check_proxy(proxy_list)