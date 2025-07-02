from django.shortcuts import render, redirect

def chat_accueil(request):
    return render(request, 'chat/chat_accueil.html')

