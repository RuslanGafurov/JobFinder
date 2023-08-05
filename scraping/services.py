import os
import sys

import django


def from_cyrillic_to_latin(text: str) -> str:
    cyrillic_letters = {
        u'а': u'a',
        u'б': u'b',
        u'в': u'v',
        u'г': u'g',
        u'д': u'd',
        u'е': u'e',
        u'ё': u'e',
        u'ж': u'zh',
        u'з': u'z',
        u'и': u'i',
        u'й': u'y',
        u'к': u'k',
        u'л': u'l',
        u'м': u'm',
        u'н': u'n',
        u'о': u'o',
        u'п': u'p',
        u'р': u'r',
        u'с': u's',
        u'т': u't',
        u'у': u'u',
        u'ф': u'f',
        u'х': u'h',
        u'ц': u'ts',
        u'ч': u'ch',
        u'ш': u'sh',
        u'щ': u'sch',
        u'ъ': u'',
        u'ы': u'y',
        u'ь': u'',
        u'э': u'e',
        u'ю': u'yu',
        u'я': u'ya'
    }
    text = text.replace(' ', '_').lower()
    result = ''
    for char in text:
        result += cyrillic_letters.get(char, char)
    return result


def get_filter(city: str, language: str) -> dict[str, str]:
    _filter = {}
    if city or language:
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
    return _filter


headers = [
    {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (HTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
]


def launch_django() -> None:
    """ Функция предназначенная для запуска Django вне приложений """
    project_path = os.path.dirname(os.path.abspath('manage.py'))
    sys.path.append(project_path)
    os.environ["DJANGO_SETTINGS_MODULE"] = 'job_finder.settings'
    django.setup()
