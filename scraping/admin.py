from django.contrib import admin

from scraping.models import City, Error, Language, Suggestion, Url, Vacancy

admin.site.register(City)
admin.site.register(Language)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Расширенное отображения модели вакансий"""

    list_display = ('site', 'title', 'city', 'language')
    fields = ('title', 'company', 'description', ('city', 'language'), 'url')
    readonly_fields = ('city', 'language')
    ordering = ('site',)


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    """Расширенное отображения модели адресов"""

    list_display = ('city', 'language')
    fields = ('urls',)
    readonly_fields = ('city', 'language')


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    """Расширенное отображения модели ошибок"""

    list_display = ('site', 'error', 'timestamp')
    fields = ('error', 'city', 'language', 'url')
    readonly_fields = ('site', 'error', 'city', 'language', 'url')
    ordering = ('timestamp',)


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    """Расширенное отображения модели предложений"""

    list_display = ('email', 'timestamp')
    fields = ('city', 'language')
    readonly_fields = ('email',)
    ordering = ('-timestamp',)
