from django.urls import path

from scraping.views import VacancyListView

urlpatterns = [
    path('list/', VacancyListView.as_view(), name='list'),
]
