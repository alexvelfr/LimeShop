from django.forms import Form, CharField, TextInput, PasswordInput
from django.core.exceptions import ValidationError
from lk.models import User


def only_digits(value):
    if not value.isdigit():
        raise ValidationError('Введенное значение содержит не только цифры', params={'value': value})


class SetPhoneForm(Form):
    phone_number = CharField(max_length=20, widget=TextInput(attrs={
        'class': 'form-control',
        'required': '',
        'placeholder': 'Введите номер телефона'
    }), validators=[only_digits])
    password = CharField(max_length=150, widget=PasswordInput(attrs={
        'class': 'form-control',
        'required': '',
        'placeholder': 'Введите пароль'
    }))
    confirm_password = CharField(max_length=150, widget=PasswordInput(attrs={
        'class': 'form-control',
        'required': '',
        'placeholder': 'Подтвердите пароль'
    }))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Form, self).clean()
        password = cleaned_data.get("password")
        phone_number = cleaned_data.get("phone_number")
        confirm_password = cleaned_data.get("confirm_password")
        errors = []
        if password != confirm_password:
            errors.append(ValidationError(
                "Введеные пароли не совпадают"
            ))
        founded_user = User.objects.filter(phone_number=phone_number).first()
        if founded_user and founded_user != self.user:
            errors.append(ValidationError(
                "Номер телефона уже занят"
            ))
        if errors:
            raise ValidationError(errors)
