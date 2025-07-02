from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('logout', views.logout_view, name='logout')
]