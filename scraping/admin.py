from django.contrib import admin

from scraping.models import City, Error, Language, Url, Vacancy

admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)
