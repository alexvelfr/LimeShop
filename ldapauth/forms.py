from django.forms import Form, CharField, TextInput
from django.core.exceptions import ValidationError


def only_digits(value):
    if not value.isdigit():
        raise ValidationError('Введенное значение содержит не только цифры', params={'value': value})


class SetPhoneForm(Form):
    phone_number = CharField(max_length=20, widget=TextInput(attrs={
        'class': 'form-control',
        'required': '',
        'numb'
        'placeholder': 'Введите номер телефона'
    }), validators=[only_digits])
