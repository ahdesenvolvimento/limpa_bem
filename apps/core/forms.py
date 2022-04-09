from django import forms
from .models import Atendimento, Cliente, Servico
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = '__all__'