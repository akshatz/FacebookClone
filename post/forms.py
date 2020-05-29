from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    date_of_birth = forms.DateTimeField(label='Date of birth', widget=DateInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2', 'first_name', 'last_name']

