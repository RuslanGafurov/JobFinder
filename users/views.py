from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


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
        new_user.set_password(form.cleaned_data['password2'])
        new_user.save()
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
                return redirect('users:update')
        else:
            form = UserUpdateForm(initial={
                'city': user.city,
                'language': user.language,
                'send_email': user.send_email,
            })
        return render(request, 'users/update.html', {'form': form})
    else:
        return redirect('users:login')
