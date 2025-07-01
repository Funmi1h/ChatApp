from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .validators import ForbiddenStartCharacterValidator, PasswordValidator
from .managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    email = None
    username = models.CharField(
        max_length=  155, 
        unique= True, 
        validators= [ForbiddenStartCharacterValidator()]
        )
    
    password = models.CharField(
        max_length= 128,
    )

    first_name = models.CharField(
        max_length= 155, 
        verbose_name= 'Prénom', 
        blank= True, 
        null= True
        )
    
    last_name= models.CharField(
        max_length= 155, 
        verbose_name= 'Nom', 
        blank= True, 
        null= True
        )
    
    numero_telephone = PhoneNumberField(
        unique= True,
        blank= False,
        null= False
    )
    
    profile_picture = models.ImageField(
        blank= True, 
        null= True, 
        upload_to= 'media/profile_pics'
        )
    



    # Le numero de telephone sera définit comme le champ d'authentification principal
    USERNAME_FIELD = 'numero_telephone'
    # Les champs requis lors de la création d'un superuser
    REQUIRED_FIELDS =[first_name, last_name, numero_telephone]
    #on utilise le manager personnalisé
    objects = CustomUserManager()
    def __str__(self):
        return self.username or self.numero_telephone