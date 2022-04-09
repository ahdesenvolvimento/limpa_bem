from django.urls import path
from .views import *

urlpatterns = [
    path('criar/', criar_usuario, name="criar_usuario"),
    path('index/', index_usuarios, name="index_usuarios"),
    path('editar/<int:pk>', editar_usuario, name="editar_usuario"),
    path('deletar/<int:pk>', deletar_usuario, name="deletar_usuario"),
    path('editar/senha/<int:pk>', editar_senha, name="editar_senha"),
]