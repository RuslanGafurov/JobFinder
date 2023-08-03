from http import HTTPStatus
from random import randint

import requests
from bs4 import BeautifulSoup

from scraping.services import headers

__all__ = (
    'headhunter',
)


def headhunter(url):
    jobs, errors = [], []
    response = requests.get(url, headers=headers[randint(0, 2)])
    if response.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', attrs={'id': 'a11y-main-content'})
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
            if div_list:
                for div in div_list:
                    title = div.find('h3').span.a
                    _url = title['href']
                    company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                    description = ''
                    jobs.append({
                        'url': _url,
                        'title': title.text,
                        'company': company.text,
                        'description': description,
                    })
            else:
                errors.append({'url': url, 'title': 'Div list does not exist'})
        else:
            errors.append({'url': url, 'title': 'Main div does not exist'})
    else:
        errors.append({'url': url, 'title': 'Page not responding'})
    return jobs, errors
