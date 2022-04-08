from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from apps.core.models import Atendimento, Cliente, Servico
from apps.usuarios.models import Atendente
from .forms import AtendimentoForm, ClienteForm, ServicoForm

# Create your views here.
@login_required(login_url='login')
def index(request):
    print(request.user.is_superuser)
    return render(request, 'index.html')

@login_required(login_url='login')
def index_servicos(request):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    if request.method == 'GET':
        servicos = Servico.objects.all()
    context = {
        'servicos':servicos
    }
    return render(request, 'core/servicos/index.html', context)

@login_required(login_url='login')
def criar_servicos(request):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão para acessar esta tela.')
        return redirect('index')
    if request.method == 'POST':
        form = ServicoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso.')
            return redirect('index_servicos')
    return render(request, 'core/servicos/form.html')

@login_required(login_url='login')
def editar_servico(request, pk):
    try:
        if not request.user.is_superuser:
            messages.info(request, 'Você não tem permissão para acessar esta tela.')
            return redirect('index')
        servico = Servico.objects.get(id=pk)
        if request.method == 'POST':
            form = ServicoForm(request.POST or None, instance=servico)
            if form.is_valid():
                form.save()
                messages.success(request, 'Serviço editado com sucesso.')
                return redirect('index_servicos')
        context = {
            'servico':servico
        }
        return render(request, 'core/servicos/form.html', context)
    except Servico.DoesNotExist:
        messages.error(request, 'Serviço não cadastrado.')
        return redirect('index_servicos')

@login_required(login_url='login')
def deletar_servico(request, pk):
    try:
        if not request.user.is_superuser:
            messages.info(request, 'Você não tem permissão realizar esta ação.')
            return redirect('index')
        servico = Servico.objects.get(id=pk)
        servico.delete()
        messages.success(request, 'Serviço deletado com sucesso.')
    except Servico.DoesNotExist:
        messages.error(request, 'Serviço não cadastrado.')
    return redirect('index_servicos')
    

@login_required(login_url='login')
def criar_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            return redirect('index_clientes')
    return render(request, 'core/clientes/form.html')

@login_required(login_url='login')
def index_clientes(request):
    context = {
        'clientes':Cliente.objects.all()
    }
    return render(request, 'core/clientes/index.html', context)


@login_required(login_url='login')
def editar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(id=pk)
        if request.method == 'POST':
            form = ClienteForm(request.POST or None, instance=cliente)
            if form.is_valid():
                form.save()
                messages.success(request, 'Serviço editado com sucesso.')
                return redirect('index_clientes')
        context = {
            'cliente':cliente
        }
        return render(request, 'core/clientes/form.html', context)
    except Servico.DoesNotExist:
        messages.error(request, 'Cliente não cadastrado.')
        return redirect('index_clientes')


@login_required(login_url='login')
def deletar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(id=pk)
        cliente.delete()
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não cadastrado.')
    return redirect('index_clientes')


@login_required(login_url='login')
def criar_atendimentos(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atendimento cadastrado com sucesso.')
            return redirect('index_atendimentos')
    # print(form.errors)
    context = {
        'atendentes':Atendente.objects.all(),
        'servicos':Servico.objects.filter(status=True),
        'clientes':Cliente.objects.all()
    }
    return render(request, 'core/atendimentos/form.html', context)

@login_required(login_url='login')
def index_atendimentos(request):
    context = {
        'atendimentos':Atendimento.objects.all()
    }
    return render(request, 'core/atendimentos/index.html', context)


@login_required(login_url='login')
def editar_atendimento(request, pk):
    try:
        atendimento = Atendimento.objects.get(id=pk)
        if request.method == 'POST':
            form = AtendimentoForm(request.POST or None, instance=atendimento)
            if form.is_valid():
                form.save()
                messages.success(request, 'Atendimento editado com sucesso.')
                return redirect('index_atendimentos')
        context = {
            'atendimento':atendimento,
            'atendentes':Atendente.objects.all(),
            'servicos':Servico.objects.filter(status=True),
            'clientes':Cliente.objects.all()
        }
        return render(request, 'core/atendimentos/form.html', context)
    except Servico.DoesNotExist:
        messages.error(request, 'Atendimento não cadastrado.')
        return redirect('index_atendimentos')


@login_required(login_url='login')
def deletar_atendimento(request, pk):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão realizar esta ação.')
        return redirect('index')
    try:
        atendimento = Atendimento.objects.get(id=pk)
        atendimento.delete()
    except Atendimento.DoesNotExist:
        messages.error(request, 'Atendimento não cadastrado.')
    return redirect('index_atendimentos')