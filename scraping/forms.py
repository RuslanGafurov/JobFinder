from django import forms

from scraping.models import City, Language


class VacancyFindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=False,
        label='Город',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name='slug',
        required=False,
        label='Специальность',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
