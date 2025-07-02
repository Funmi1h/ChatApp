from django.urls import path
from . import views 
urlpatterns =[
    path('chat_accueil/',views.chat_accueil, name = 'chat_accueil' )
]