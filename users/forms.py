from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    """Форма входа"""

    email = forms.EmailField(
        label='Адрес',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес электронной почты',
        }),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        }),
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            current_user = User.objects.filter(email=email)
            if not current_user.exists():
                raise forms.ValidationError('Такого пользователя нет')
            if not check_password(password, current_user[0].password):
                raise forms.ValidationError('Не правильно введён пароль')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""

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
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']


class UserUpdateForm(forms.Form):
    """Форма редактирования данных"""

    city = forms.ModelChoiceField(
        label='Город',
        queryset=City.objects.all(),
        to_field_name='slug',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    language = forms.ModelChoiceField(
        label='Язык',
        queryset=Language.objects.all(),
        to_field_name='slug',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    send_email = forms.BooleanField(
        label='Получать рассылку?',
        required=False,
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email')


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
