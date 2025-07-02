from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.phonenumber import PhoneNumber

#Pour gérer les utilisateurs de facon personnalisé en l'identifiant avec son numer de telephone
class CustomUserManager(BaseUserManager):

    use_in_migrations = True # Pour que le manager soit correctement géré par les migrations

    def create_user(self, numero_telephone, password = None, **extra_fields):
        if not numero_telephone:
            raise ValueError (_('Le numéro de téléphone doit être renseigné. '))
        

        if not password:
            raise ValueError(_('Le mot de passe doit être renseigné.'))

        if not isinstance(numero_telephone, PhoneNumber):
            try:
                numero_telephone = PhoneNumber.from_string(phone_number= str(numero_telephone))


            except Exception:
                raise ValueError (_('Le numéro de téléphone n\'est pas valide.'))

        user = self.model(numero_telephone = numero_telephone,  **extra_fields)

        #Gestion des mots de passe
       
        user.set_password(password)
        user.save(using = self._db) # Pour s'assurer que l'objet est sauvegardé dans la base de données que celle sur laquelle le gestionnaire opere

        return user


    def create_superuser(self, numero_telephone, password = None,  **extra_fields):
        # Mettre tous les flags du superuser a True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        #S'assurer que tous les flags sont a true 

        if extra_fields.get('is_staff')  is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_staff a True'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_superuser a True'))

        if extra_fields.get('is_active') is not True:
            raise ValueError (_('Le superutilisateur doit etre actif'))        
        
        return self.create_user(numero_telephone, password, **extra_fields)