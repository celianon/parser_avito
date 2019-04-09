import requests
from bs4 import BeautifulSoup
from read_config import headers
from get_proxy import proxy


url = 'http://sitespy.ru/my-ip'

r = requests.get(url, headers=headers, proxies={'http' : f'http://{proxy}'},)

if r.status_code == 200:
	soup = BeautifulSoup(r.text, 'lxml')
	ip = soup.find('span', class_='ip').text
	user_agent = soup.find('span', style='font-size: 20px;').text.split('User-Agent:')[1].strip()
	print(user_agent)
	print(f'Ваш ip {ip}')
