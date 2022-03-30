from abc import ABC

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import RegexValidator

LATIN_CYRILLIC_STRING_REGEX = '^[a-zA-Zа-яА-ЯЩЬьЮюЯяЇїІіЄєҐґ]+$'
UA_PHONE_NUMBER_REGEX = '^380[0-9]{9}$'


class CyrillicRegexMixin(ABC):
    regex = LATIN_CYRILLIC_STRING_REGEX


class NameValidator(CyrillicRegexMixin, RegexValidator):
    message = 'Имя должно состоять только из букв латиницы или кириллицы.'


class SurnameValidator(CyrillicRegexMixin, RegexValidator):
    message = 'Фамилия должна состоять только из букв латиницы или кириллицы.'


class PatronymicValidator(CyrillicRegexMixin, RegexValidator):
    message = 'Отчество должно состоять только из букв латиницы или кириллицы.'


class PhoneNumberValidator(RegexValidator):
    message = 'Номер телефона должен быть длинной в 12 символов и начинаться с 380.'
    regex = UA_PHONE_NUMBER_REGEX


class SquareImageValidator:
    message = "Изображение должно быть квадратным"

    def __call__(self, image, close=False):
        width, height = get_image_dimensions(image, close=close)
        if width == height:
            return image
        else:
            raise ValidationError(self.message)
