from django.forms import ModelForm
from .models import Atendimento, Cliente, Servico
class ServicoForm(ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class AtendimentoForm(ModelForm):
    class Meta:
        model = Atendimento
        fields = '__all__'