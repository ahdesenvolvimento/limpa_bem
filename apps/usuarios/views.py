from pyclbr import Function
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, Group
from django.contrib import messages

from apps.usuarios.forms import AtualizaAtendenteForm, AtualizaGerenteForm, AtualizaSenha, CadastroFuncionarioForm, CadastroGerenteForm
from apps.usuarios.models import Gerente, Pessoa, Usuario

# Create your views here.
@login_required(login_url='login')
def criar_usuario(request):
    if str(request.method == 'POST'):
        tipo_funcionario = request.POST.get('is_superuser')
        if tipo_funcionario:
            form = CadastroGerenteForm(request.POST or None)
        else:
            form = CadastroFuncionarioForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('index_usuarios')
    context = {
        'form':form,
        'groups':Group.objects.all()
    }
    return render(request, 'usuarios/form.html', context)

@login_required(login_url='login')
def editar_usuario(request, pk):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    try:
        usuario = Pessoa.objects.get(id=pk)
        if str(request.method == 'POST'): 
            if usuario.is_superuser:
                form = AtualizaGerenteForm(request.POST or None, instance=usuario)
            else:
                form = AtualizaAtendenteForm(request.POST or None, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, "Usuário atualizado com sucesso!")
                return redirect('index_usuarios')
        context = {
            'edit':True,
            'usuario':usuario
        }
        return render(request, 'usuarios/form.html', context)
    except Usuario.DoesNotExist:
        messages.error(request, 'Este usuário não está cadastrado no sistema.')
        return redirect('index_usuarios')

@login_required(login_url='login')
def editar_senha(request, pk):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    try:
        usuario = Usuario.objects.get(id=pk)
        if str(request.method == 'POST'): 
            form = AtualizaSenha(request.POST or None, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, "Senha alterada com sucesso!")
                return redirect('index_usuarios')
        else:
            form = AtualizaSenha(instance=usuario)
        context = {
            'form':form
        }
        return render(request, 'usuarios/form_senha.html', context)
    except Usuario.DoesNotExist:
        messages.error(request, 'Este usuário não está cadastrado no sistema.')
        return redirect('index_usuarios')

@login_required(login_url='login')
def deletar_usuario(request, pk):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    try:
        if str(request.method == 'POST'):
            usuario = Usuario.objects.get(id=pk)
            usuario.delete()
            messages.success(request, 'Usuario deletado com sucesso!')
            return redirect('index_usuarios')
    except Usuario.DoesNotExist:
        messages.error(request, 'Este usuário não está cadastrado no sistema.')
        return redirect('index_usuarios')

@login_required(login_url='login')
def index_usuarios(request):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    context = {
        'funcionarios':Pessoa.objects.all()
    }
    return render(request, 'usuarios/index.html', context)