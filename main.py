import requests
import os
import argparse
from dotenv import load_dotenv

def make_short_link(token, url):
    url_bit_ly = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    payload = {'long_url': url}
    response = requests.post(url_bit_ly, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(token, bitlink):
    url_bit_ly = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=bitlink)
    payload = {'unit': 'day',
                'units': -1
                }
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(url_bit_ly, params=payload, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']

def check_link(token, url):
    url_bit_ly = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'.format(bitlink=url)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(url_bit_ly, headers=headers)
    return response.ok

def parse_arguments():
    help = '''Короткая ссылка bit.ly или длинная ссылка для обработки
Пример короткой ссылки: bit.ly/2Iw9i4X
Пример длинной ссылки: https://yandex.ru'''
    parser = argparse.ArgumentParser(description='Аналитака ссылок bit.ly', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('url', help=help)
    args = parser.parse_args()
    return args.url

if __name__ == '__main__':
    url = parse_arguments()
    load_dotenv()
    token = os.getenv('TOKEN')
    try:
        if check_link(token, url):
            print('Число переходов по ссылке {}'.format(count_clicks(token, url)))
        else:
            print(make_short_link(token, url))
    except requests.exceptions.HTTPError as http_error:
        print('The request failed', http_error, "Сheck the link is correct", sep='\n')