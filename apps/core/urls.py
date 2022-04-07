from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('servicos/index/', index_servicos, name="index_servicos"),
    path('servicos/criar/', criar_servicos, name="criar_servicos"),
    path('servicos/editar/<int:pk>', editar_servico, name="editar_servico"),
    path('servicos/deletar/<int:pk>', deletar_servico, name="deletar_servico"),

    path('clientes/index/', index_clientes, name="index_clientes"),
    path('clientes/criar/', criar_clientes, name="criar_clientes"),
    path('clientes/editar/<int:pk>', editar_cliente, name="editar_cliente"),
    path('clientes/deletar/<int:pk>', deletar_cliente, name="deletar_cliente"),

    path('atendimentos/index/', index_atendimentos, name="index_atendimentos"),
    path('atendimentos/criar/', criar_atendimentos, name="criar_atendimentos"),
    path('atendimentos/editar/<int:pk>', editar_atendimento, name="editar_atendimento"),
    path('atendimentos/deletar/<int:pk>', deletar_atendimento, name="deletar_atendimento"),

]