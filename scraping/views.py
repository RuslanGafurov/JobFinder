from django.shortcuts import render
from django.views.generic import ListView

from scraping.forms import VacancyFindForm
from scraping.models import Vacancy
from scraping.services import get_filter


def home_view(request):
    """Отображение домашней страницы с формой поиска"""
    form = VacancyFindForm()
    return render(request, 'home.html', {'form': form})


class VacancyListView(ListView):
    """Отображение вакансий"""
    model = Vacancy
    paginate_by = 10
    template_name = 'scraping/list.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyListView, self).get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = VacancyFindForm()
        return context

    def get_queryset(self):
        _filter = get_filter(
            self.request.GET.get('city'),
            self.request.GET.get('language')
        )
        return Vacancy.objects.filter(**_filter)
