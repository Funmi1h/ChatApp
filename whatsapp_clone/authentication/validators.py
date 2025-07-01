from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _





class ForbiddenStartCharacterValidator:
    def __init__(self, minlenght= 3, maxlenght= 20):
        self.minlenght = minlenght
        self.maxlenght = maxlenght
    

    def __call__(self, value):
        self.value = value
        if not re.search(r'\s', value ):
            raise ValidationError(_('Votre username ne doit pas contenir d\'espace'))

        if  self.minlenght > len(value)  or self.maxlenght  >len(value) :
            raise ValidationError(_('Votre username doit contenir entre 3 et 20 cractères'))







class PasswordValidator:
    def __init__(self, minlength = 8):
        self.minlength = minlength

    def __call__(self, password):
        self.password = password
        # le mot de passe doit contenir au moins une lettre majuscule
        if not any(password.isupper()):
            raise ValidationError(_('Le mot de passe doit contenir au moins une lettre majuscule.'))
        
        # le mot de passe doit contenir au moins une lettre miniscule
        if not any(password.islower()):
            raise ValidationError(_('Le mot de passe doit contenir au moins une lettre minuscule.'))
        
        # le mot de passe doit contenir au moins minlength caracteres
        if len(password) < self.minlenght:
            raise ValidationError(_(f'Le mot de passe doit contenir au moins {self.minlenght}'))

        # le mot de passe doit contenir au moins un chiffre
        if not re.search(r'\d', password):
            raise ValidationError (_('Le mot de passe doit contenir au moins un chiffre'))
        
        # le mot de passe doit contenir au moins un caractere spécial

        if not re.search(r'[^a-zA-Z0-9\s]', password):
            raise ValidationError(_('Le mot de passe doit contenir au moins un caractère spécial')) 

            