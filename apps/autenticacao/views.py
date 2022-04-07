from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Permission, Group
from django.contrib import messages


def login_page(request):
    if str(request.method == 'POST'):
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        if senha != None and usuario != None:
            user = authenticate(request, username=usuario, password=senha)
            if user is None:
                messages.error(request, 'Usuario não cadastrado, favor checar suas credenciais!')
                return redirect('login')
            else:
                login(request, user)
                return redirect('index')
    return render(request, 'login/login.html')

@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')

