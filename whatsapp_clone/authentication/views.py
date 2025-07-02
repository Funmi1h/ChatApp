from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.utils.translation import gettext_lazy as _
import authentication.forms as forms
from django.contrib import messages



class LoginView(View):
    template_name = 'authentication/login.html'
    
    def get(self, request):
        form = forms.LoginForm()
        return render (request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        form.request = request
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat_accueil')
        else:
            messages.error(request, _('Mot de passe ou numéro de téléphone invalide'))
        return render(request, self.template_name,{'form': form} )
    

class SignUpView(View):
    template_name = 'authentication/signup.html'

    def get(self, request):
        form = forms.SignUpForm()
        return render (request, self.template_name, {'form': form})
    
    def post(self, request):
        form = forms.SignUpForm(request.POST) 
        form.request = request
        if form.is_valid():
            # Créer une instance de user sans le sauvegarder
            user = form.save(commit= False)
            #hashe le mot de passe
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Tu es prêt pour blablater!!')
            return redirect('chat_accueil')
        else:
            messages.error(request, 'Corriges les erreurs du formulaire 😔' )         
            
        return render(request, self.template_name, {'form': form})
               



def logout_view(request):
    logout(request)
    messages.info(request, 'Tu pars 😔? Bon à toute 😊!')