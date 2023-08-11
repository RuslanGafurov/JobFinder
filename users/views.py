from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from scraping.models import Suggestion
from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, UserContactForm

User = get_user_model()


def login_view(request):
    """Вход в аккаунт"""
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        cln_data = form.cleaned_data
        user = authenticate(
            request,
            email=cln_data.get('email'),
            password=cln_data.get('password')
        )
        login(request, user)
        messages.success(request, 'Вход в аккаунт выполнен')
        return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    messages.success(request, 'Выход из аккаунта выполнен')
    return redirect('home')


def registration_view(request):
    """Регистрация пользователя"""
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password2'])
        new_user.save()
        messages.success(request, 'Аккаунт зарегистрирован')
        return render(request, 'users/registration_done.html', {'new_user': new_user})
    return render(request, 'users/registration.html', {'form': form})


def update_view(request):
    """Обновление данных аккаунта"""
    contact_form = UserContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                cln_data = form.cleaned_data
                user.city = cln_data['city']
                user.language = cln_data['language']
                user.send_email = cln_data['send_email']
                user.save()
                messages.success(request, 'Данные изменены')
                return redirect('users:profile')
        else:
            form = UserUpdateForm(initial={
                'city': user.city,
                'language': user.language,
                'send_email': user.send_email,
            })
        forms = {'form': form, 'contact_form': contact_form}
        return render(request, 'users/profile.html', forms)
    return redirect('users:login')


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
