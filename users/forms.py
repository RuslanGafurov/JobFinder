from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from scraping.models import City, Language
from users.models import User


class UserLoginForm(AuthenticationForm):
    """Форма входа"""

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        }),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        }),
    )
    email = forms.EmailField(
        label='Адрес',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес электронной почты',
        }),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        }),
    )
    password2 = forms.CharField(
        label='Повторный пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        return super(UserRegistrationForm, self).save(commit=commit)


class UserProfileForm(UserChangeForm):
    """Форма профиля пользователя"""

    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    email = forms.EmailField(
        label='Адрес',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес электронной почты',
        }),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name='slug',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    send_email = forms.BooleanField(
        label='Получать рассылку?',
        required=False,
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'city', 'language', 'send_email')


class UserContactForm(forms.Form):
    """Форма предложений от пользователя"""

    city = forms.CharField(
        label='Город',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    language = forms.CharField(
        label='Специальность',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    email = forms.EmailField(
        label='Введите адрес электронной почты',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
    )
