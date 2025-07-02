from .models import User
from django.http import request
from django.utils.translation import gettext_lazy as _
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    numero_telephone = PhoneNumberField(label = _('Numéro de téléphone'))
    password = forms.CharField(max_length= 155, 
        label= _('Mot de passe'), 
        widget= forms.PasswordInput()
    )

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


        # Vérifier les identifiants sans connecter directement l'utilisateur
        if  numero_telephone and password:
            self.user = authenticate(
                request= request,
                numero_telephone = numero_telephone
            )

        # Gérer les résultats de l'authentification si les identifiants ne correspondent pas a un utilisateur
        if self.user is None:
            raise ValidationError(
                _('Ton numéro de téléphone et/ou ton mot de passe est invalide(s)'),
                code='invalid_login'
                )
        

        #Récupérer l'utilisateur authentifié apres que le form.is_valid() est True

    def get_user(self):
        return getattr(self, 'user', None)



class SignUpForm(forms.ModelForm):

    confirm_password = forms.CharField(
        max_length= 123,
        widget= forms.PasswordInput(),
        required= True
    )
    class Meta:
        model = User
        fields = ['numero_telephone', 'username', 'last_name', 'first_name', 'password']

    
    

        labels = {
            'numero_telephone': 'Numéro de téléphone',
                'username': 'Nom d\'utilisateur',
                'last_name': 'Nom',
                'first_name': 'Prénom(s)',
                'password': 'Mot de passe',
                'confirm_password': 'Confirmes le mot de passe'
                }
        

        helps_texts = {
            'password':_('Le mot de passe doit contenir au moins 8 caractères dont au moins une lettre majuscule, au moins une lettre miniscule, au moins un carctère spécial et au moins un chiffre'),
            'username': _('Ton username doit contenir entre 3 et 20 caractères et ne doit pas contenir d\'espace '),
        }

        widgets = {
                'numero_telephone': forms.TextInput(),
                'username': forms.TextInput(),
                'last_name': forms.TextInput(),
                'first_name': forms.TextInput(),
                'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero_telephone'].required = True
        self.fields['username'].required = True
        self.fields['password'].required = True
    
    def clean(self):

        cleaned_data = super().clean()
        # Unicité du numéro de téléphone
        numero = cleaned_data.get('numero_telephone')
        if User.objects.filter(numero_telephone = numero).exists():
            self.add_error('numero_telephone', _('Ce numéro de téléphone est déjà utilisé'))
        
        #correspondance des mots de passe
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password',_('Les mots de passe ne correspondent pas'))

        return cleaned_data