from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/criar/', criar_usuario, name="criar_usuario"),
    path('usuarios/index/', index_usuarios, name="index_usuarios"),
    path('usuarios/editar/<int:pk>', editar_usuario, name="editar_usuario"),
    path('usuarios/deletar/<int:pk>', deletar_usuario, name="deletar_usuario"),
    path('usuarios/editar/senha/<int:pk>', editar_senha, name="editar_senha"),
]