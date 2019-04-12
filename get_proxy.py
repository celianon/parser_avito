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
	for i in range(len(proxy_list)):
		global proxy
		proxy = choice(proxy_list)
		proxy = {'https' : f'https://{proxy}'}
		try:
			r = requests.get('https://avito.ru', verify=True, headers=headers , proxies=proxy, timeout=5)
			if r.status_code == 200:
				print(f'Использованная прокси : {proxy.get("https")}')
				return proxy

		except :
			print(f'Не удалось подключиться с {proxy.get("https")}')
			proxy_list.remove(str(proxy.get("https")[8:]))
			if proxy_list == []:
				print('Прокси закончились ')
				sys.exit(0)
			continue
		

proxy = check_proxy(proxy_list)