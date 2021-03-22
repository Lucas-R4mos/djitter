from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.entrar, name='entrar'),
    path('logon/', views.inscrever, name='inscrever'),
    path('logon2/', views.inscrever2, name='inscrever2'),
    path('logon3/', views.inscrever3, name='inscrever3'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('novoPost/', views.novoPost, name='novoPost'),
    path('@<str:username>/', views.perfil, name='perfil')
]