import os
import sys
from configparser import ConfigParser


# Find config path
base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, "config.ini")

# Check correct path
if os.path.exists(config_path):
    cfg = ConfigParser()
    cfg.read(config_path)
else:
    print("Config( %s ) not found! Exiting!" % config_path)
    sys.exit(1)


site_url = 'https://www.avito.ru/ekaterinburg/vakansii/bez_opyta_studenty'
result = []
filter_result = []
FROM = cfg.get('email', 'FROM')
TO = cfg.get('messege', 'TO')
PASSWORD = cfg.get('email', 'PASSWORD')
SUBJECT = cfg.get('messege', 'SUBJECT')
headers = {'User-Agent': 'Mozilla/6.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
more = cfg.get('filter', 'more')
less = cfg.get('filter', 'less')
proxy = cfg.get('path', 'proxy')
api_key = cfg.get('api', 'key')

if not less:
	less = 100000000000000

if not more:
	more = 0

