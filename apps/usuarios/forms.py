from pyclbr import Function
from django import forms
from .models import *

class CadastroGerenteForm(forms.ModelForm):

    class Meta:
        model = Gerente
        fields = ('nome', 'logradouro', 'cep', 'localidade', 'bairro', 'complemento', 'telefone', 'cpf', 'numero', 'email', 'username', 'password', 'is_superuser')

    def save(self, commit=True):
        user = super(CadastroGerenteForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user

class CadastroFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Atendente
        fields = ('nome', 'logradouro', 'cep', 'localidade', 'bairro', 'complemento', 'telefone', 'cpf', 'numero', 'email', 'username', 'password', 'is_superuser')
    
    def save(self, commit=True):
        user = super(CadastroFuncionarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
