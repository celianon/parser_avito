import requests
from read_config import proxy
from random import choice

with open(proxy) as p:
	proxy = p.read().split('\n')
	for i, data in enumerate(proxy):
		proxy[i] = data.replace('\t', ':')

proxy = choice(proxy)