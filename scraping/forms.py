from django import forms

from scraping.models import Vacancy, City, Language


class VacancyFindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=False,
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name='slug',
        required=False,
    )
