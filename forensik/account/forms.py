from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    error_messages = {
        "password_mismatch": "Die eingegebenen Kennwörter stimmen nicht überein.",
        "email_used": "Es wurde bereits ein Nutzer mit dieser E-Mail-Adresse registriert.",
    }

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','is_superuser','is_staff']
        labels = {
            "is_superuser": "Forensiker",
            "is_staff": "Bitte ankreuzen",
            "first_name": "Vorname",
            "last_name": "Nachname",
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Benutzername'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Vorname'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nachname'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Passwort'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Passwort wiederholen'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'E-Mailadresse eingeben'})
        self.fields['is_superuser']
        self.fields['is_staff']