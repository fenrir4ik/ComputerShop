from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from apps.user.models import User
from core.db.user_dao import UserDao
from utils import form_validators


class UserBaseForm(forms.Form):
    """Base form with user data and validators for every field"""
    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
        validators=[form_validators.name_validator],
        max_length=45
    )
    surname = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        validators=[form_validators.surname_validator],
        max_length=45
    )
    patronymic = forms.CharField(
        label="Отчество",
        widget=forms.TextInput(attrs={'placeholder': 'Отчество'}),
        validators=[form_validators.patronymic_validator],
        max_length=45
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.TextInput(attrs={'placeholder': 'Почта'})
    )
    phone_number = forms.CharField(
        label="Номер телефона",
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
        required=False,
        empty_value=None,
        validators=[form_validators.phone_number_validator],
        max_length=12
    )


class RegistrationForm(UserBaseForm, UserCreationForm):
    """Form is used for user registration"""

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'name', 'surname', 'patronymic', 'password1', 'password2')

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    def __init__(self, *args, **kwargs):
        """Fixes browser autofocus on username field which is email in current user model"""
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})

    def clean_email(self):
        """Replace validation error message when user with given email address already exists"""
        user_email = self.cleaned_data.get('email')
        try:
            UserDao.get_user_by_email(user_email)
            raise forms.ValidationError('Адресс электронной почты используется другим пользователем.')
        except User.DoesNotExist:
            return user_email


class LoginForm(AuthenticationForm):
    """Form is used to authorize user"""

    def __init__(self, *args, **kwargs):
        """Changes invalid_login error message"""
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False, 'placeholder': 'Адресс электронной почты'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})
        self.error_messages['invalid_login'] = "Введенные данные не верны. Проверьте данные и попробуйте снова."


class ProfileChangeForm(UserBaseForm, forms.ModelForm):
    """Form is used to change user profile information"""
    password1 = forms.CharField(validators=[validate_password], widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('name', 'surname', 'patronymic', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        """Fixes password autocomplete when profile change form loads"""
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'

    def clean_email(self):
        """Replace validation error message when user with given email address already exists"""
        user_email = self.cleaned_data.get('email')
        try:
            user = UserDao.get_user_by_email(user_email)
            if self.instance.email != user_email:
                raise forms.ValidationError('Адресс электронной почты используется другим пользователем.')
            else:
                return user_email
        except User.DoesNotExist:
            return user_email

    def save(self, commit=True):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            self.instance.set_password(password2)
        return super().save()

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают')
