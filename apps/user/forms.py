from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from apps.user.models import User
from services import user_service
from utils import form_validators


class UserBaseForm():
    pass

class RegistrationForm(UserCreationForm):
    """Form is used for user registration"""

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
        validators=[form_validators.name_validator]
    )
    surname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        validators=[form_validators.surname_validator]
    )
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Отчество'}),
        validators=[form_validators.patronymic_validator]
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Почта'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
        required=False,
        empty_value=None,
        validators=[form_validators.phone_number_validator]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

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
            user_service.get_user_by_email(user_email)
            raise forms.ValidationError('Адресс электронной почты используется другим пользователем.')
        except User.DoesNotExist:
            return user_email


class LoginForm(AuthenticationForm):
    """Form is used to authorize user"""

    def __init__(self, *args, **kwargs):
        """Changes invalid_login error message"""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False, 'placeholder': 'Адресс электронной почты'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})
        self.error_messages['invalid_login'] = "Введенные данные не верны. Проверьте данные и попробуйте снова."


class ProfileChangeForm(UserChangeForm):
    """Form is used to change user profile information"""
    class Meta:
        model = User
        fields = ('name', 'surname', 'patronymic', 'email', 'phone_number')

    name = forms.CharField(validators=[form_validators.name_validator])
    surname = forms.CharField(validators=[form_validators.surname_validator])
    patronymic = forms.CharField(validators=[form_validators.patronymic_validator])
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
        required=False,
        empty_value=None,
        validators=[form_validators.phone_number_validator]
    )

    def clean_email(self):
        """Replace validation error message when user with given email address already exists"""
        user_email = self.cleaned_data['email']
        try:
            user = user_service.get_user_by_email(user_email)
            if self.instance.email != user_email:
                raise forms.ValidationError('Адресс электронной почты используется другим пользователем.')
            else:
                return user_email
        except User.DoesNotExist:
            return user_email
    # TODO think about user change form or inherit from UserRegisterForm, p1 p2 think