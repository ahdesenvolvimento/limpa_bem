from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Sum
from django.contrib import messages

from apps.core.models import Atendimento, Cliente, Servico
from apps.usuarios.models import Atendente
from .forms import AtendimentoForm, ClienteForm, ServicoForm

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML

from datetime import datetime
from dateutil.relativedelta import relativedelta

import os

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):
    data_atual = datetime.today() + relativedelta(days=+1)
    print(data_atual)
    six_months = data_atual.today() + relativedelta(days=-6)
    print(data_atual)
    print(six_months)
    print(Atendimento.objects.get(id=6).criado)
    print(Atendimento.objects.filter(criado__range=[six_months, data_atual.strftime('%Y-%m-%d')]).values('criado__month').annotate(contador=Count('criado')))
    # sampledate__gte=datetime.date(2011, 1, 1),
    #                             sampledate__lte=datetime.date(2011, 1, 31)
    # print(Atendimento.objects.filter(criado__month=data_atual.month).aggregate(Sum('valor_pago')))
    total = 0
    for i in Atendimento.objects.filter(criado__month=data_atual.month):
        print(i.valor_pago.replace(',',''))
        total += float(i.valor_pago.replace(',',''))
    print(total)
    context = {
        'qnt_cliente':Cliente.objects.filter(criado__month=data_atual.month),
        'total_faturado':total#Atendimento.objects.filter(criado__month=data_atual.month).aggregate(Sum('valor_pago'))
    }
    return render(request, 'core/dashboard.html', context)

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
                messages.success(request, 'Cliente editado com sucesso.')
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
        messages.success(request, 'Cliente deletado com sucesso.')
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
        messages.success(request, 'Atendimento deletado com sucesso.')
    except Atendimento.DoesNotExist:
        messages.error(request, 'Atendimento não cadastrado.')
    return redirect('index_atendimentos')



@login_required(login_url='login')
def gerar_relatorios(request):
    if not request.user.is_superuser:
        messages.info(request, 'Você não tem permissão acessar esta tela.')
        return redirect('index')
    if request.method == 'POST':
        tipo_relatorio = request.POST.get('relatorio')
        data_atual = datetime.today()
        dir = 'apps/media/relatorios/'
        if tipo_relatorio == '1':
            atendimentos = Atendimento.objects.filter(criado__contains=datetime.today().strftime('%Y-%m-%d'))
            dados = {
                'atendimentos':Atendimento.objects.filter(criado__contains=datetime.today().strftime('%Y-%m-%d')),
                'total':sum([float(i.valor_pago.replace(',', '')) for i in atendimentos]),
                'data_relatorio':data_atual
            }
            pdf = relatorio_pdf(
                    request, 
                    'core/relatorios/lista_atendimentos_dia.html', 
                    dados,
                    dir,
                    'lista_atendimentos_dia'
            )
        elif tipo_relatorio == '2':
            atendimentos = Atendimento.objects.filter(criado__month=data_atual.month)
            dados = {
                'atendimentos': atendimentos,
                'total':sum([float(i.valor_pago.replace(',', '')) for i in atendimentos]),
                'data_relatorio':data_atual
            }
            pdf = relatorio_pdf(
                    request, 
                    'core/relatorios/lista_atendimentos_mes.html', 
                    dados,
                    dir,
                    'lista_atendimentos_mes'
            )
        elif tipo_relatorio == '3':
            atendimentos = Atendimento.objects.filter(criado__month=data_atual.month).values('id_funcionario', 'id_funcionario__nome').annotate(dcount=Count('id_funcionario')).order_by()
            dados = {
                'atendimentos': atendimentos,
                'data_relatorio':data_atual
            }
            pdf = relatorio_pdf(
                    request, 
                    'core/relatorios/qnt_atendimentos_funcionarios.html', 
                    dados,
                    dir,
                    'qnt_atendimentos_funcionarios'
            )
        elif tipo_relatorio == '4':
            atendimentos = Atendimento.objects.filter(criado__month=data_atual.month).values('id_cliente', 'id_cliente__nome').annotate(dcount=Count('id_cliente')).order_by()
            dados = {
                'atendimentos':atendimentos,
                'data_relatorio':data_atual
            }
            pdf = relatorio_pdf(
                    request, 
                    'core/relatorios/lista_clientes_fieis.html', 
                    dados,
                    'apps/media/relatorios/',
                    'lista_clientes_fieis'
                )
        return pdf
    return render(request, 'core/relatorios/form.html')

def relatorio_pdf(request, dir_template, dados, dir_relatorios, nome_pdf):
    html_string = render_to_string(
        dir_template, dados
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    # dir = 'apps/media/relatorios/'
    dir = dir_relatorios
    check_dir(dir)

    html.write_pdf(target='{}/{}.pdf'.format(dir, nome_pdf), presentational_hints=True)
    fs = FileSystemStorage(dir)
    with fs.open('{}.pdf'.format(nome_pdf)) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline: filename="relatorio.pdf"'
    return response

def check_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)



# html_string = render_to_string(
#                 'core/relatorios/qnt_atendimentos_funcionarios.html', 
#                 {
#                     'atendimentos': Atendimento.objects.filter(criado__month=data_atual.month).values('id_funcionario', 'id_funcionario__nome').annotate(dcount=Count('id_funcionario')).order_by()
#                 }
#             )
#             html = HTML(string=html_string, base_url=request.build_absolute_uri())
#             dir = 'apps/media/relatorios/'
#             check_dir(dir)

#             html.write_pdf(target='{}/qnt_atendimentos_funcionarios.pdf'.format(dir), presentational_hints=True)
#             fs = FileSystemStorage('apps/media/relatorios/')
#             with fs.open('qnt_atendimentos_funcionarios.pdf') as pdf:
#                 response = HttpResponse(pdf, content_type='application/pdf')
#                 response['Content-Disposition'] = 'inline: filename="relatorio.pdf"'
#             return response