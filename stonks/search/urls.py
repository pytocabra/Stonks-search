from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='search/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='search/logout.html'), name='logout'),
    path('liked/', views.liked, name='liked')
]