from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _





class ForbiddenStartCharacterValidator:
    def __init__(self, minlenght= 3, maxlenght= 20):
        self.minlenght = minlenght
        self.maxlenght = maxlenght
    

    def __call__(self, value):
        self.value = value
        if ' ' in value:
            raise ValidationError(_('Votre username ne doit pas contenir d\'espace'))

        if not( self.minlenght < len(value)  or len(value) < self.maxlenght ):
            raise ValidationError(_('Votre username doit contenir entre 3 et 20 cractères'))






class PasswordValidator:
    def validate(self, password, user=None):
        # longueur minimale du mot de passe
        if len(password) < 8:
            raise ValidationError(
                _("Le mot de passe doit contenir au moins 8 caractères."),
                code='password_too_short',
            )

        # le mot de passe doit contenir une lettre majuscule minimum
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une majuscule."),
                code='password_no_upper',
            )

        # au moins un chiffre

        if not re.search(r'\d', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre."),
                code='password_no_digit',
            )

        # Caractère spécial
        if not re.search(r'[!@#$%^&*()_+=\[{\]};:<>|./?,-]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Votre mot de passe doit contenir au moins 8 caractères, une majuscule, un chiffre et un caractère spécial."
        )