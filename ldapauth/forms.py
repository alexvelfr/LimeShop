from django.forms import Form, CharField, TextInput


class SetPhoneForm(Form):
    phone_number = CharField(max_length=20, widget=TextInput(attrs={
        'class': 'form-control',
        'required': '',
        'placeholder': 'Введите номер телефона'
    }))
