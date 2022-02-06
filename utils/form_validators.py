from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import RegexValidator

latin_cyrillic_string_regex = '^[a-zA-Zа-яА-ЯЩЬьЮюЯяЇїІіЄєҐґ]+$'
ua_phone_number_regex = '^380[0-9]{9}$'


def name_validator(name):
    return RegexValidator(latin_cyrillic_string_regex,
                          'Имя должно состоять только из букв латиницы или кириллицы.')(name)


def surname_validator(surname):
    return RegexValidator(latin_cyrillic_string_regex,
                          'Фамилия должна состоять только из букв латиницы или кириллицы.')(surname)


def patronymic_validator(patronymic):
    return RegexValidator(latin_cyrillic_string_regex,
                          'Отчество должно состоять только из букв латиницы или кириллицы.')(patronymic)


def phone_number_validator(phone_number):
    return RegexValidator(
        ua_phone_number_regex,
        'Номер телефона должен быть длинной в 12 символов и начинаться с 380.')(phone_number)


def square_image_validator(image):
    width, height = get_image_dimensions(image)
    if width == height:
        return image
    else:
        raise ValidationError("Изображение должно быть квадратным")
