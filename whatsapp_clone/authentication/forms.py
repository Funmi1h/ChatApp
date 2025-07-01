from .models import User
from django.http import request
from django.utils.translation import gettext_lazy as _
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    numero_telephone = PhoneNumberField(label = _('Numéro de téléphone'))
    password = forms.CharField(max_length= 155, 
        label= _('Mot de passe'), 
        widget= forms.PasswordInput(attrs= {
            'placeholder' : _('Votre mot de passe')
        }))

    # init pour personnaliser le comportement du formulaire des sa création
    # init sert a initialiser une instance de class
    # xa sert a récupérer des parametres supplementaires comme request et initialiser des variables d'instances comme self.user = None
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        numero_telephone = cleaned_data.get('numero_telephone')
        password = cleaned_data.get('password')

        if  numero_telephone and password:
            self.user = authenticate(
                request= request,
                numero_telephone = numero_telephone
            )
    
