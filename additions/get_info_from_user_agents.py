import requests
import json

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import read_config


user_agets = input('Введите User-Agents >>> ')
api_url = 'https://api.whatismybrowser.com/api/v2/user_agent_parse'
post_data = {
        "user_agent": user_agets
    }

def get_info():

    headers = {'X-API-KEY': read_config.api_key}  # paste your api-key here
    result = requests.post(api_url,
                           data=json.dumps(post_data),
                           headers=headers)
    dict_ = result.json().get('parse')

    for key in dict_:
        print(f'{key}  :  {dict_[key]}')


if __name__ == '__main__':
    get_info()
