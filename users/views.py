from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from users.forms import UserLoginForm, UserRegistrationForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def registration_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(request, 'users/login.html', {'new_user': new_user})
    return render(request, 'users/registration.html', {'form': form})
