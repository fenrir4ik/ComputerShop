from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from apps.user.models import User
from apps.user.services import get_user_by_field_value
from core.regexps import latin_cyrillic_string, ua_phone_number


class RegistrationForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
        validators=[
            RegexValidator(latin_cyrillic_string, 'Имя должно состоять только из букв латиницы или кириллицы.')
        ]
    )
    surname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        validators=[
            RegexValidator(latin_cyrillic_string, 'Фамилия должна состоять только из букв латиницы или кириллицы.')
        ]
    )
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Отчество'}),
        validators=[
            RegexValidator(latin_cyrillic_string, 'Отчество должно состоять только из букв латиницы или кириллицы.')
        ]
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Почта', 'autofocus': 'False'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
        validators=[
            RegexValidator(ua_phone_number, 'Номер телефона должен быть длинной в 12 символов и начинаться с 380.')
        ]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'name', 'surname', 'patronymic', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """Fixes browser autofocus on username field which is email in current user model"""
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})

    def clean_email(self):
        """Replace validation error message when user with given email address already exists"""
        user_email = self.cleaned_data['email']
        try:
            get_user_by_field_value('email', user_email)
            raise forms.ValidationError('Адресс электронной почты используется другим пользователем.')
        except User.DoesNotExist:
            return user_email

    def clean_phone_number(self):
        """Replace validation error message when user with given phone number already exists"""
        user_phone_number = self.cleaned_data['phone_number']
        try:
            get_user_by_field_value('phone_number', user_phone_number)
            raise forms.ValidationError('Номер телефона используется другим пользователем.')
        except User.DoesNotExist:
            return user_phone_number
