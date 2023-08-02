from django.shortcuts import render
from django.views.generic import ListView

from scraping.forms import VacancyFindForm
from scraping.models import Vacancy
from scraping.services import get_filter

__all__ = (
    'home_view',
    'VacancyListView',
)


def home_view(request):
    context = {'form': VacancyFindForm()}
    return render(request, 'home.html', context)


class VacancyListView(ListView):
    model = Vacancy
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
