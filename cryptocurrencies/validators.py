from rest_framework.exceptions import ValidationError


def validate_percentage(value):
    if value < 0 or value > 100:
        raise ValidationError(f'{value} не допустимое значение процента. Оно должно быть в диапазоне от 0 до 100.')
