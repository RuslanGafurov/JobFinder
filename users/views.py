import datetime as dt

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from scraping.models import Error
from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, UserContactForm

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.success(request, 'Вход в аккаунт выполнен')
        return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Выход из аккаунта выполнен')
    return redirect('home')


def registration_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password2'])
        new_user.save()
        messages.success(request, 'Аккаунт зарегистрирован')
        return render(request, 'users/registration_done.html', {'new_user': new_user})
    return render(request, 'users/registration.html', {'form': form})


def update_view(request):
    contact_form = UserContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
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
    else:
        return redirect('users:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            user_qs = User.objects.get(pk=user.pk)
            user_qs.delete()
            messages.success(request, 'Аккаунт удален')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        contact_form = UserContactForm(request.POST or None)
        if contact_form.is_valid():
            cln_data = contact_form.cleaned_data
            city = cln_data.get('city')
            language = cln_data.get('language')
            email = cln_data.get('email')
            errors_today = Error.objects.filter(timestamp=dt.date.today())
            if errors_today.exists():
                err = errors_today.first()
                data = err.data.get('user_data', [])
                data.append({
                    'city': city,
                    'language': language,
                    'email': email,
                })
                err.data['user_data'] = data
                err.save()
            else:  # Нет ошибок за сегодняшний день
                user_data = [{
                    'city': city,
                    'language': language,
                    'email': email,
                }]
                Error(data=f'Предложения пользователей: {user_data}').save()

            messages.success(request, 'Данные отправлены')
            return redirect('users:profile')
        else:  # Форма не валидна
            return redirect('users:profile')
    else:  # Метод GET
        return redirect('users:login')
