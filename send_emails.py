# _______________ Запуск Django ________________
from scraping.services import launch_django  # |
                                             # |
launch_django()                              # |
# _____________________________________________|

import datetime as dt

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from job_finder.settings import env
from scraping.models import City, Error, Language, Url, Vacancy

User = get_user_model()


def send_messages(_subject: str, _text_content: str, html_content: str, to: str) -> None:
    """Отправка электронных писем"""

    msg = EmailMultiAlternatives(_subject, _text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def get_vacancies() -> None:
    """Формирование актуальных вакансий"""

    _subject = f'Рассылка вакансий за { today }'
    _text_content = f'Рассылка вакансий за { today }'
    empty = '<h2>К сожалению, на сегодня вакансий нет</h2>'

    # Формирование IDs городов и специальностей
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])

    vacancies_qs = Vacancy.objects.filter(**params, timestamp=today).values()  # Все вакансии за сегодня

    # Отсортированные вакансии по IDs городов и специальностей
    all_vacancies = {}
    for vacancy in vacancies_qs:
        all_vacancies.setdefault((vacancy['city_id'], vacancy['language_id']), [])
        all_vacancies[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)

    for ids, emails in users_dct.items():
        vacancies = all_vacancies.get(ids, [])  # Вакансии по определенным IDs городов и специальностей

        # Формирование html страницы для отображения вакансий
        _html = ''
        for vacancy in vacancies:
            _html += f'<h5>{ vacancy["title"] }</h5>'
            _html += f'<p>{ vacancy["company"] }</p>'
            _html += f'<p>{ vacancy["description"] }</p>'
            _html += f'<a href="{ vacancy["url"] }">Просмотреть</a><br><hr>'
        html_content = _html if _html else empty

        # Отправка списка вакансий каждому пользователю
        for email in emails:
            send_messages(subject, _text_content, html_content, email)


def get_errors(html_content: str) -> None:
    """Формирование ошибок при сборе вакансий"""

    errors_subject = f'Ошибки сбора вакансий за { today }'
    _text_content = f'Ошибки сбора вакансий за { today }'

    for err in errors_qs.values():
        # Формирование html страницы с ошибкой
        for row in err:
            html_content += f'<h5>Ошибка: {row["title"]}</h5>'
            html_content += f'<a href="{row["url"]}">Просмотреть</a><br><hr>'

            # Отправка ошибки админу
            send_messages(errors_subject, _text_content, html_content, admin_email)


def check_urls() -> tuple[str, str, str]:
    """Проверка наличия urls по наборам: город, специальность"""

    cities = City.objects.all().values('id', 'name')
    languages = Language.objects.all().values('id', 'name')
    url_html, url_subject, url_text_content, names = ('' for _ in range(4))

    # Смена IDs городов и специальностей на названия
    for ids in users_dct.keys():
        city = cities.get(pk=ids[0])['name']
        language = languages.get(pk=ids[1])['name']
        if ids not in urls_ids_dct:
            names += f' { city } - { language },'

    # Формирование отображения html страницы
    if names:
        url_html = f'Отсутствуют URLs для:{ names[:-1] }'
        url_subject = f'Отсутствующие urls за { today }'
        url_text_content = url_subject

    return url_subject, url_html, url_text_content


today = dt.date.today()
from_email = env('EMAIL_HOST_USER')
admin_email = env('EMAIL_HOST_USER')
subject, html, text_content = '', '', ''

users_qs = User.objects.filter(send_email=True).values('email', 'city', 'language')
urls_ids_qs = Url.objects.all().values('city', 'language')
errors_qs = Error.objects.filter(timestamp=today).values('data')


# Формирование словаря со списком адресов по городу и специализации
users_dct = {}
for user in users_qs:
    users_dct.setdefault((user['city'], user['language']), [])
    users_dct[(user['city'], user['language'])].append(user['email'])


# Формирование словаря с urls
urls_ids_dct = {(url['city'], url['language']): True for url in urls_ids_qs}

# Если есть IDs urls
if urls_ids_dct:
    subject, html, text_content = check_urls()

# Если есть пользователи, которым нужна рассылка
if users_dct:
    get_vacancies()

# Если имеются какие-либо ошибки
if errors_qs.exists():
    get_errors(html)
# Если нет ошибок, но отсутствуют urls
else:
    if subject:
        send_messages(subject, text_content, html, admin_email)
