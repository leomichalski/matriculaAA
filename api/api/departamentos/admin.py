from django.contrib import admin
from .models import Departamento


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    def admin_nome(self):
        return self.nome

    def admin_index(self):
        return self.index

    def admin_codigo(self):
        return self.codigo

    admin_nome.short_description = 'Nome'
    admin_index.short_description = 'Index'
    admin_codigo.short_description = 'Codigo'

    list_display = (
        admin_nome,
        admin_codigo,
    )

    search_fields = [
        'nome',
        'codigo',
    ]
