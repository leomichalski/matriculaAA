from django.contrib import admin
from .models import Discente


@admin.register(Discente)
class DiscenteAdmin(admin.ModelAdmin):
    def admin_turmas_desejadas(self):
        return self.turmas_desejadas

    def admin_matricula(self):
        return self.matricula

    def admin_senha(self):
        return self.senha

    def admin_cpf(self):
        return self.cpf

    def admin_data_de_nascimento(self):
        return self.data_de_nascimento

    def admin_email(self):
        return self.email

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ("senha", )
        return super().get_form(request, obj, **kwargs)

    admin_turmas_desejadas.short_description = 'Turmas Desejadas'
    admin_matricula.short_description = 'Matricula'
    admin_senha.short_description = 'Senha'
    admin_cpf.short_description = 'Cpf'
    admin_data_de_nascimento.short_description = 'Data de Nascimento'
    admin_email.short_description = 'Email'

    list_display = (
        admin_matricula,
        admin_data_de_nascimento,
        admin_email,
    )

    search_fields = [
        'matricula',
        'data_de_nascimento',
        'email',
    ]

    filter_horizontal = ('turmas_desejadas',)
