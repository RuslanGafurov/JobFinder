from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from scraping.models import Suggestion
from users.forms import (UserContactForm, UserLoginForm, UserProfileForm,
                         UserRegistrationForm)
from users.models import User

__all__ = (
    'UserLoginView',
    'UserRegistrationView',
    'UserProfileView',
    'delete_view',
    'contact_view',
)


class UserLoginView(SuccessMessageMixin, LoginView):
    """Вход в аккаунт"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = 'Вход в аккаунт выполнен'


class UserRegistrationView(SuccessMessageMixin, CreateView):
    """Регистрация нового пользователя"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_message = 'Аккаунт зарегистрирован. Теперь Вы можете войти'
    success_url = reverse_lazy('users:login')


class UserProfileView(SuccessMessageMixin, UpdateView):
    """Профиль пользователя"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_message = 'Данные изменены'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})


def delete_view(request):
    """Удаление аккаунта"""
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            user_qs = User.objects.get(pk=user.pk)
            user_qs.delete()
            messages.success(request, 'Аккаунт удален')
    return redirect('home')


def contact_view(request):
    """Отправка предложения от пользователя"""
    if request.method == 'POST':
        contact_form = UserContactForm(request.POST or None)
        if contact_form.is_valid():
            cln_data = contact_form.cleaned_data
            user_suggestion = Suggestion(
                city=cln_data.get('city'),
                language=cln_data.get('language'),
                email=cln_data.get('email'),
            )
            user_suggestion.save()
            messages.success(request, 'Данные отправлены')
        return redirect('users:profile')
    return redirect('users:login')
