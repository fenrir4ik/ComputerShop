from django.core.validators import RegexValidator

latin_cyrillic_string_regex = '[a-zA-Zа-яА-ЯЩЬьЮюЯяЇїІіЄєҐґ]'
ua_phone_number_regex = '^380[0-9]{9}$'

name_validator = RegexValidator(
    latin_cyrillic_string_regex,
    'Имя должно состоять только из букв латиницы или кириллицы.'
)
surname_validator = RegexValidator(
    latin_cyrillic_string_regex,
    'Фамилия должна состоять только из букв латиницы или кириллицы.'
)
patronymic_validator = RegexValidator(
    latin_cyrillic_string_regex,
    'Отчество должно состоять только из букв латиницы или кириллицы.'
)
phone_number_validator = RegexValidator(
    ua_phone_number_regex,
    'Номер телефона должен быть длинной в 12 символов и начинаться с 380.'
)
