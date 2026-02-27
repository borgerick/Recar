from django.contrib import admin

from .models import Local, Disponibilidade, Reserva

admin.site.register(Local)
admin.site.register(Disponibilidade)
admin.site.register(Reserva)