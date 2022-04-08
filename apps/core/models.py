from pyexpat import model
from django.db import models

from apps.usuarios.models import Atendente

# Create your models here.
class Base(models.Model):
    id = models.AutoField(primary_key=True)
    criado = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Servico(Base):
    nome = models.CharField("Nome do serviço", max_length=255, null=False, blank=False)
    descricao = models.CharField('Descrição breve do serviço', max_length=255, null=True, blank=True)
    valor = models.CharField('Valor do serviço', max_length=255, null=False, blank=False)
    status = models.BooleanField('Status do serviço', default=True)

    def get_valor(self):
        pass

    class Meta:
        db_table = 'servico'

class Endereco(Base):
    logradouro = models.CharField(max_length=255)
    numero = models.IntegerField(null=True, blank=True)
    cep = models.CharField(max_length=11)
    localidade = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=255, null=True, blank=False)
    class Meta:
        db_table = 'endereco'

class Cliente(Endereco):
    nome = models.CharField('Nome do cliente', max_length=255, null=False, blank=False)
    telefone = models.CharField('Telefone', max_length=20, null=False, blank=False)
    email = models.EmailField('E-mail', max_length=255, null=True)
    cpf = models.CharField('CPF', max_length=14, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'cliente'
    
class Atendimento(Base):
    OPCOES_ATENDIMENTO = (
        ('1','Pendente'),
        ('2','Realizado'),
        ('3','Cancelado')
    )
    id_servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=False, blank=False)
    id_funcionario = models.ForeignKey(Atendente, on_delete=models.CASCADE, null=False, blank=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
    valor_pago = models.CharField('Valor pago pelo cliente', max_length=255, null=False, blank=False)
    desconto = models.BooleanField('Desconto', default=False)
    data_limpeza = models.DateField('Data da limpeza', null=False, blank=False)
    situacao = models.CharField('Situação do atendimento', max_length=255, choices=OPCOES_ATENDIMENTO)

    class Meta:
        db_table = 'atendimento'

# class AtendimentoServico(Base):
#     id_atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE)
#     id_servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'atendimento_servico'

# class AtendimentoServicoEndereco(Base):
#     id_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
#     id_atendimento = models.ForeignKey(AtendimentoServico, on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'atendimento_servico_endereco'
