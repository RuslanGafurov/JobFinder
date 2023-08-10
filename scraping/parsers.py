from http import HTTPStatus
from random import randint
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup

from scraping.services import headers

return_annotation = tuple[list[dict[str, Any]], list[dict[str, str]]]


def headhunter(url: str, city: Optional[int] = None, language: Optional[int] = None) -> return_annotation:
    jobs, errors = [], []
    if url:
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
                            'city_id': city,
                            'language_id': language,
                        })
                else:
                    errors.append({'url': url, 'title': 'Div list does not exist'})
            else:
                errors.append({'url': url, 'title': 'Main div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page not responding'})
    return jobs, errors
