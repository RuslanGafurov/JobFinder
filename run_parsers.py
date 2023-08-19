# _____________ Запуск Django ______________
from scraping.services import launch_django

launch_django()
# __________________________________________

import asyncio
import datetime as dt
from typing import Any

from django.db import DatabaseError

from scraping.models import Error, Url, Vacancy
from scraping.parsers import *

parsers = (
    (headhunter, 'headhunter'),
    (super_job, 'super_job'),
    (rabota_ru, 'rabota_ru'),
    (zarplata_ru, 'zarplata_ru'),
)
jobs, errors = [], []
today = dt.date.today()


def get_urls() -> list[dict[str, Any]]:
    """ Функция получения адресов пользователей для поиска вакансий """

    urls_qs = Url.objects.all().values()
    urls = []
    for user in urls_qs:
        urls.append({
            'city': user['city_id'],
            'language': user['language_id'],
            'urls': user['urls'],
        })
    return urls


def save_errors() -> None:
    """Сохранение ошибок в Базу Данных без дубликатов"""

    for error_dct in errors:
        # Добавление новой ошибки или обновление существующей
        Error.objects.update_or_create(
            site=error_dct['site'],
            error=error_dct['error'],
            url=error_dct['url'],
            defaults={'error': error_dct['error']}  # Обновляемое значение
        )


url_lst = get_urls()


# ________________________ Асинхронный запуск функций ________________________
async def main(value: tuple[Any, str, int, int]) -> None:
    func, url, city, language = value
    _job, _error = await loop.run_in_executor(None, func, url, city, language)
    errors.append(_error)
    jobs.extend(_job)


loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['urls'][key], data['city'], data['language'])
             for data in url_lst
             for func, key in parsers]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()
# ____________________________________________________________________________

# Сохранение полученных вакансий
for job in jobs:
    vacancy = Vacancy(**job)
    try:
        vacancy.save()
    except DatabaseError:
        pass

# Проверка наличия ошибок и вызов функции сохранения
if errors[0]:
    save_errors()


# Удаление неактуальных вакансий
ten_days_ago = today - dt.timedelta(days=10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
