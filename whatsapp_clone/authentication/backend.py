from .models import User
from django.contrib.auth.backends import BaseBackend
class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, numero_telephone = ..., password = ..., **kwargs):
        user = User.objects.get(numero_telephone = numero_telephone)
        return user
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk =user_id)
            return user
        except User.DoesNotExist:
            return None

 