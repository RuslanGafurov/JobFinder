from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, render

from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

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
        return render(request, 'users/profile.html', {'form': form})
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
