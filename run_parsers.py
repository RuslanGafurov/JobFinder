import os
import sys

from django.db import DatabaseError

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ["DJANGO_SETTINGS_MODULE"] = 'job_finder.settings'

import django

django.setup()

from scraping.models import City, Language, Vacancy
from scraping.parsers import *

parsers = (
    (headhunter, 'https://kursk.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=Python&excluded_text=&area=2'
                 '&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0'
                 '&items_on_page=50'),
)

city = City.objects.filter(slug='sankt-peterburg').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []
for func, url in parsers:
    jbs, errs = func(url)
    jobs += jbs
    errors += errs

for job in jobs:
    vacancy = Vacancy(**job, city=city, language=language)
    try:
        vacancy.save()
    except DatabaseError:
        pass


# # ____________________________________ Test ____________________________________
# import codecs
#
# with codecs.open(filename='headhunter.txt', mode='w', encoding='utf-8') as file:
#     file.write(str(jobs))
