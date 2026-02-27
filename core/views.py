from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Local, Disponibilidade, Reserva
from datetime import datetime, time


# =====================
# PAGINAS PRINCIPAIS
# =====================

def principal(request):
    return render(request, "core/principal.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Autenticar o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login bem-sucedido
            auth_login(request, user)
            messages.success(request, f"Bem-vindo, {user.first_name or user.username}!")
            return redirect("home")
        else:
            # Credenciais inválidas
            messages.error(request, "Usuário ou senha inválidos!")
            return redirect("login")
    
    return render(request, "core/login.html")


def home(request):
    return render(request, "core/home.html")


def cadastro_usuario(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # Validação de senhas iguais
        if password != password2:
            messages.error(request, "As senhas não conferem!")
            return redirect("cadastro_usuario")

        # Verificar se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Este usuário já existe!")
            return redirect("cadastro_usuario")

        # Criar usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name
        )

        messages.success(request, "Cadastro realizado com sucesso! Agora faça login.")
        return redirect("login")

    return render(request, "core/cadastro_usuario.html")


# =====================
# LOCAIS
# =====================

def local_listar(request):
    locais = Local.objects.all()
    return render(request, "core/local_listar.html", {"locais": locais})


def local_novo(request):
    if request.method == "POST":

        # CRIA O LOCAL
        local = Local.objects.create(
            nome=request.POST.get("nome"),
            cidade=request.POST.get("cidade"),
            rua=request.POST.get("rua"),
            numero=request.POST.get("numero"),
            estado=request.POST.get("estado"),
            pais=request.POST.get("pais"),
            cep=request.POST.get("cep"),
        )
        
        hoje = datetime.today().date()

        for hora in range(24):
            Disponibilidade.objects.create(
                local=local,
                data=hoje,
                hora=time(hour=hora, minute=0),
                disponivel=True
            )

        return redirect("local_listar")

    return render(request, "core/local_novo.html")


def local_editar(request, id):
    local = Local.objects.get(id=id)

    if request.method == "POST":
        local.nome = request.POST.get("nome")
        local.cidade = request.POST.get("cidade")
        local.rua = request.POST.get("rua")
        local.numero = request.POST.get("numero")
        local.estado = request.POST.get("estado")
        local.pais = request.POST.get("pais")
        local.cep = request.POST.get("cep")
        local.save()

        return redirect("local_listar")

    return render(request, "core/local_editar.html", {"local": local})


def excluir_local(request, id):
    Local.objects.get(id=id).delete()
    return redirect("local_listar")


# =====================
# DISPONIBILIDADE (COM FILTRO POR DATA)
# =====================

def disponibilidade(request):

    data_escolhida = request.GET.get("data")
    disponibilidade = []

    if data_escolhida:
        try:
            data_convertida = datetime.strptime(data_escolhida, "%Y-%m-%d").date()

            disponibilidade = Disponibilidade.objects.filter(
                data=data_convertida,
                disponivel=True
            ).select_related("local")

        except:
            disponibilidade = []

    return render(
        request,
        "core/disponibilidade.html",
        {
            "disponibilidade": disponibilidade,
            "data_escolhida": data_escolhida
        }
    )


# =====================
# RESERVAS
# =====================

def minha_reserva_listar(request):
    reserva = Reserva.objects.all()
    return render(request, "core/minha_reserva_listar.html", {"reserva": reserva})


def minha_reserva_nova(request):

    # FILTRO DE DATA
    data_escolhida = request.GET.get("data")

    disponibilidades = None

    if data_escolhida:
        disponibilidades = Disponibilidade.objects.filter(
            data=data_escolhida,
            disponivel=True
        ).select_related("local")

    # CRIAR RESERVA
    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect("login")

        disp_id = request.POST.get("disponibilidade")

        try:
            disp = Disponibilidade.objects.get(id=disp_id, disponivel=True)

            Reserva.objects.create(
                disponibilidade=disp,
                usuario=request.user
            )

            # BLOQUEIA HORÁRIO
            disp.disponivel = False
            disp.save()

            return redirect("minha_reserva_listar")

        except Disponibilidade.DoesNotExist:
            pass

    return render(
        request,
        "core/minha_reserva_nova.html",
        {
            "disponibilidade": disponibilidades,
            "data_escolhida": data_escolhida
        }
    )


def minha_reserva_editar(request, id):
    reserva = Reserva.objects.get(id=id)
    
    # FILTRO DE DATA
    data_escolhida = request.GET.get("data")
    disponibilidades = None
    
    if data_escolhida:
        disponibilidades = Disponibilidade.objects.filter(
            data=data_escolhida,
            disponivel=True
        ).select_related("local")
    
    # ATUALIZAR RESERVA
    if request.method == "POST":
        disp_id = request.POST.get("disponibilidade")
        
        try:
            nova_disp = Disponibilidade.objects.get(id=disp_id, disponivel=True)
            
            # LIBERA A DISPONIBILIDADE ANTERIOR
            reserva.disponibilidade.disponivel = True
            reserva.disponibilidade.save()
            
            # ATUALIZA PARA NOVA DISPONIBILIDADE
            reserva.disponibilidade = nova_disp
            reserva.save()
            
            # BLOQUEIA NOVA DISPONIBILIDADE
            nova_disp.disponivel = False
            nova_disp.save()
            
            return redirect("minha_reserva_listar")
        
        except Disponibilidade.DoesNotExist:
            pass
    
    return render(
        request,
        "core/minha_reserva_editar.html",
        {
            "reserva": reserva,
            "disponibilidade": disponibilidades,
            "data_escolhida": data_escolhida
        }
    )


def minha_reserva_excluir(request, id):
    reserva = Reserva.objects.get(id=id)
    
    # LIBERA A DISPONIBILIDADE
    reserva.disponibilidade.disponivel = True
    reserva.disponibilidade.save()
    
    # DELETA A RESERVA
    reserva.delete()
    
    return redirect("minha_reserva_listar")