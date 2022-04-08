from pyclbr import Function
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, Group
from django.contrib import messages

from apps.usuarios.forms import CadastroFuncionarioForm, CadastroGerenteForm
from apps.usuarios.models import Gerente, Usuario

# Create your views here.
@login_required(login_url='login')
def criar_usuario(request):
    # if request.user.check_permission('accounts.add_usuario'):
    #     messages.info(request, 'Você não tem permissão!')
    #     return redirect('index')
    # if not Group.objects.filter().first():
    #     messages.info(request, 'Não existe cargos cadastrados no sistema.')
    #     return redirect('listar_usuarios')
    if str(request.method == 'POST'):
        tipo_funcionario = request.POST.get('is_superuser')
        print(tipo_funcionario)
        if tipo_funcionario:
            form = CadastroGerenteForm(request.POST or None)
        else:
            print('to aqui')
            form = CadastroFuncionarioForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            print('to aqui')
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            # my_group = Group.objects.get(id=request.POST.get('groups'))
            # my_group.user_set.add(user)
            return redirect('index')
    context = {
        'form':form,
        'groups':Group.objects.all()
    }
    return render(request, 'usuarios/form.html', context)

@login_required(login_url='login')
def editar_usuario(request, pk):
    # if request.user.check_permission('accounts.change_usuario'):
    #     messages.info(request, 'Você não tem permissão!')
    #     return redirect('index')
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    try:
        usuario = Usuario.objects.get(id=pk)
        # usuario = Gerente.objects.get(id=pk) if usuario.is_superuser else Aten.objects.get(id=pk)
        if str(request.method == 'POST'): 
            form = AtualizaCadastro(request.POST or None, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, "Usuário atualizado com sucesso!")
                return redirect('list_users')
        else:
            form = AtualizaCadastro(instance=usuario)
        context = {
            'form':form,
            'edit':True,
            'groups':Group.objects.all(),
            'group_user':usuario.groups.all().first(),
        }
        return render(request, 'accounts/user/form_user.html', context)
    except Usuario.DoesNotExist:
        messages.error(request, 'Este usuário não está cadastrado no sistema.')
        return redirect('list_users')

@login_required(login_url='login')
def editar_senha(request, pk):
    # if request.user.check_permission('accounts.change_usuario'):
    #     messages.info(request, 'Você não tem permissão!')
    #     return redirect('index')
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
                return redirect('list_users')
        else:
            form = AtualizaSenha(instance=usuario)
        context = {
            'form':form
        }
        return render(request, 'accounts/user/edit_password.html', context)
    except Usuario.DoesNotExist:
        messages.error(request, 'Este usuário não está cadastrado no sistema.')
        return redirect('list_users')

@login_required(login_url='login')
def deletar_usuario(request, pk):
    # if request.user.check_permission('accounts.delete_usuario'):
    #     messages.info(request, 'Você não tem permissão!')
    #     return redirect('index')
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
    # if request.user.check_permission('accounts.view_usuario'):
    #     messages.info(request, 'Você não tem permissão!')
    #     return redirect('index')
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    context = {
        'usuarios':Usuario.objects.all()
    }
    return render(request, 'usuarios/index.html', context)