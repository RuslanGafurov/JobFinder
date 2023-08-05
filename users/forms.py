from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):

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
