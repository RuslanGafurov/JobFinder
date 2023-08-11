# _______________ Запуск Django ________________
from scraping.services import launch_django  # |
                                             # |
launch_django()                              # |
# _____________________________________________|

import asyncio
import datetime as dt
from typing import Any

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from scraping.models import Error, Url, Vacancy
from scraping.parsers import headhunter

User = get_user_model()

parsers = (
    (headhunter, 'headhunter'),
)
jobs, errors = [], []
today = dt.date.today()


def get_settings() -> set[tuple[int, int]]:
    """ Функция получения IDs города и языка """

    users_qs = User.objects.filter(send_email=True).values()
    ids = set((u['city_id'], u['language_id']) for u in users_qs)
    return ids


def get_urls(_settings: set[tuple[int, int]]) -> list[dict[str, Any]]:
    """ Функция получения адресов пользователей для поиска вакансий """

    urls_qs = Url.objects.all().values()
    url_dct = {(u['city_id'], u['language_id']): u['urls_data'] for u in urls_qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            urls.append({
                'city': pair[0],
                'language': pair[1],
                'urls_data': url_dct[pair],
            })
    return urls


settings = get_settings()
url_lst = get_urls(settings)


# __________________________ Асинхронный запуск функций __________________________
async def main(value: tuple[Any, str, int, int]) -> None:                       # |
    func, url, city, language = value                                           # |
    _job, _error = await loop.run_in_executor(None, func, url, city, language)  # |
    errors.extend(_error)                                                       # |
    jobs.extend(_job)                                                           # |
                                                                                # |
                                                                                # |
loop = asyncio.get_event_loop()                                                 # |
tmp_tasks = [(func, data['urls_data'][key], data['city'], data['language'])     # |
             for data in url_lst                                                # |
             for func, key in parsers]                                          # |
                                                                                # |
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])            # |
                                                                                # |
loop.run_until_complete(tasks)                                                  # |
loop.close()                                                                    # |
# ________________________________________________________________________________|

# Сохранение полученных вакансий
for job in jobs:
    vacancy = Vacancy(**job)
    try:
        vacancy.save()
    except DatabaseError:
        pass

# Проверка наличия ошибок и их сохранение
if errors:
    errors_today = Error.objects.filter(timestamp=today)
    # За текущий день
    if errors_today.exists():
        err = errors_today.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        data = f'errors: {errors}'
        Error(data=data).save()

# Удаление неактуальных вакансий
ten_days_ago = today - dt.timedelta(days=10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
