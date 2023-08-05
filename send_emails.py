# _______________ Запуск Django ________________
from scraping.services import launch_django  # |
                                             # |
launch_django()                              # |
# _____________________________________________|

from job_finder.settings import env

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from scraping.models import Vacancy

User = get_user_model()


users = User.objects.filter(send_email=True).values('email', 'city', 'language')

subject = 'Рассылка вакансий'
text_content = 'Рассылка вакансий'
from_email = env('EMAIL_HOST_USER')
empty = '<h2>К сожалению, на сегодня вакансий нет./h2>'
users_dct = {}
for user in users:
    users_dct.setdefault((user['city'], user['language']), [])
    users_dct[(user['city'], user['language'])].append(user['email'])

if users_dct:
    params = {
        'city_id__in': [],
        'language_id__in': [],
    }
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    vacancies_qs = Vacancy.objects.filter(**params).values()[:10]
    vacancies = {}
    for vacancy in vacancies_qs:
        vacancies.setdefault((vacancy['city_id'], vacancy['language_id']), [])
        vacancies[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5>{ row["title"] }</h5>'
            html += f'<p>{ row["company"] }</p>'
            html += f'<p>{ row["description"] }</p>'
            html += f'<a href="{ row["url"] }">Просмотреть</a><br><hr>'
        html_content = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
