import requests
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

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
    if response.ok:
        return 'Число переходов по ссылке {}'.format(count_clicks(token, url))
    else:
        return make_short_link(token, url)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Аналитака ссылок bit.ly')
    parser.add_argument('url', help='Короткая ссылка bit.ly или длинная ссылка для обработки')
    args = parser.parse_args()
    return args.url

if __name__ == '__main__':
    url = parse_arguments()
    token = os.getenv('TOKEN')
    long_link = 'https://www.youtube.com/' # long link example
    short_link ='bit.ly/2WUrzNe' # short link example
    try:
        print(check_link(token, url))     
    except requests.exceptions.HTTPError as http_error:
        print('The request failed', http_error, "Сheck the link is correct", sep='\n')