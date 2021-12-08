from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Почта')
    username = forms.CharField(label='Логин', required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)