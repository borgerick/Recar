from django.db import models
from django.contrib.auth.models import User


class Local(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    cep = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} - {self.cidade}"


class Disponibilidade(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.local.nome} - {self.data} {self.hora}"


class Reserva(models.Model):
    
    disponibilidade = models.ForeignKey(Disponibilidade, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.username} - {self.disponibilidade}"