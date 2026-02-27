"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import (
    principal, login, home, cadastro_usuario,
    local_listar, local_novo, local_editar, excluir_local,
    disponibilidade,
    minha_reserva_listar, minha_reserva_nova, minha_reserva_editar, minha_reserva_excluir,
    logout
)

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", principal, name="principal"),
    path("login/", login, name="login"),
    path("home/", home, name="home"),
    path("cadastro/", cadastro_usuario, name="cadastro_usuario"),

    path("locais/", local_listar, name="local_listar"),
    path("locais/novo/", local_novo, name="local_novo"),
    path("locais/editar/<int:id>/", local_editar, name="local_editar"),
    path("locais/excluir/<int:id>/", excluir_local, name="excluir_local"),

    path("disponibilidade/", disponibilidade, name="disponibilidade"),
    path("logout/", logout, name="logout"),

    path("reservas/", minha_reserva_listar, name="minha_reserva_listar"),
    path("reservas/nova/", minha_reserva_nova, name="minha_reserva_nova"),
    path("reservas/editar/<int:id>/", minha_reserva_editar, name="minha_reserva_editar"),
    path("reservas/excluir/<int:id>/", minha_reserva_excluir, name="minha_reserva_excluir"),
]