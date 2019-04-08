import requests
from bs4 import BeautifulSoup
from codecs import open
import json
import csv
import xlwt
import os # 
import sys # 
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from multiprocessing import Pool #
import pdb


from read_config import *
from get_proxy import proxy


def soup(url):
	session = requests.Session()
	request = session.get(url, headers=headers, proxies={'http' : proxy}, timeout=10)

	if request.status_code == 200:

		soup = BeautifulSoup(request.content, 'lxml')

		print(proxy)

		if soup != None:
			print(f'Успешное соединение с {url}')
		return soup
	else:
		print(f'Ошибка подключения.\n Код состояния: {request.status_code}')
		exit()


# get count of pages
def get_pages(soup):
	last_page_list = soup.findAll('a', class_='pagination-page')
	for item in last_page_list:
		if item.string == 'Последняя':
			last_page = item
			pages = int(last_page.get('href')[-1])
			break
	print(f'Количество страниц: {pages}')
	return pages


# get info on each page
def pars(site_url, pages):
	for page in range(pages):
		site_url = f'{site_url}?p={page+1}'
		page_response = requests.get(site_url)
		page_content = page_response.content

		soup = BeautifulSoup(page_content, 'lxml')

		info = soup.findAll('div', class_='description item_table-description')

		for i in info:
			title = i.contents[1].contents[1].contents[1].contents[1].string
			prise = i.contents[1].contents[3].contents[2].get('content')
			result.append({'title': title,'prise': prise})

	if result != None:
		print(f'Успешно спаршено {len(result)} данных')



def filter():
	for i in result:
		if int(less) > int(i.get('prise')) > int(more):
			filter_result.append(i)
	print(f'Данные успешно профильтрованы. Осталось {len(filter_result)} ')


def create_json():
	with open('data.json', 'w', 'utf-8') as file:
		json.dump(filter_result, file, ensure_ascii=False)
	


def create_xls():

	font0 = xlwt.Font()
	font0.name = 'Times New Roman'
	font0.colour_index = 0
	font0.bold = True

	style0 = xlwt.XFStyle()
	style0.font = font0

	wb = xlwt.Workbook()
	ws = wb.add_sheet('Avito', cell_overwrite_ok=True)
	# pdb.set_trace()
	ws.col(0).width = 13689

	ws.write(0, 0, 'Title', style0)
	ws.write(0, 1, 'Prise', style0)

	

	for i, data in enumerate(filter_result):
		
		ws.write( i+1, 0, data.get('title') )
		ws.write( i+1, 1, int(data.get('prise')) )
		

	wb.save('data.xls')



def create_csv():
	with open('data.csv', 'w',encoding='cp1251') as file:
		csvwriter = csv.writer(file, delimiter=';')
		count = 0

		for i in filter_result:

			if count == 0:
					header = i.keys()
					csvwriter.writerow(header)
					count += 1

			csvwriter.writerow(i.values())
	print('Cоздан файл data.csv!')			

def send_email():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(FROM, PASSWORD)

	msg = MIMEMultipart("alternative")
	msg["Subject"] = SUBJECT
	msg["From"] = FROM
	msg["To"] = TO

	filename = 'data.xls'

	with open(filename, 'rb') as file:
		part2 = MIMEBase("application", "octet-stream")
		part2.set_payload(file.read())

	encoders.encode_base64(part2)
	part2.add_header(
		"Content-Disposition",
		f"attachment; filename= {filename}",
	)

	html = f'''
	<!DOCTYPE html>
	<html lang="en">
		<head>
			<meta charset="UTF-8">
			<title>Document</title>
		</head>
		<body>
			<h3>Привет, я парсер</h3>
			<p>Это полученные данные с сайта {site_url}</p>
		</body>
	</html>
	'''
	
	part = MIMEText(html, "html")
	msg.attach(part2)
	msg.attach(part)

	try:
		server.sendmail('kostya.nik.3854@gmail.com', ['kostya.nik.3854@gmail.com'], msg.as_string())
		print(f'Сообщение на адрес {TO} успешно отправлено!')
	except:
		print('Не удалось отправить сообщение!')
		server.quit()



# def do_all(pages):
# 	pars(site_url, pages)


# with Pool(20) as p:
# 	p.map(do_all, get_pages(soup(site_url))
# )


def main():

	pages_count = get_pages(soup(site_url))
	pars(site_url, pages_count)

	filter()

	if cfg.get('do', 'json') == '1':
		try:
			create_json()
			print('Создан файл data.json! ')
		except:
			print('Не удалось создать файл data.json! ')
	
	if cfg.get('do', 'csv') == '1':
		try:
			create_csv()
			print('Создан файл data.csv! ')
		except:
			print('Не удалось создать файл data.csv! ')
		

	if cfg.get('do', 'xls') == '1':
		try:
			create_xls()
			print('Создан файл data.xls! ')
		except:
			print('Не удалось создать файл data.xls! ')

	if cfg.get('do', 'email') == '1':
		send_email()



main()