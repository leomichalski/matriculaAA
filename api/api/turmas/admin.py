from django.contrib import admin
from .models import Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    def admin_nome_disciplina(self):
        return self.nome_disciplina

    def admin_codigo_disciplina(self):
        return self.codigo_disciplina

    def admin_nome_docente(self):
        return self.nome_docente

    def admin_horario_codificado(self):
        return self.horario_codificado

    def admin_quantidade_de_vagas(self):
        return self.quantidade_de_vagas

    def admin_departamento(self):
        return self.departamento

    admin_nome_disciplina.short_description = 'Nome Disciplina'
    admin_codigo_disciplina.short_description = 'Codigo Disciplina'
    admin_nome_docente.short_description = 'Nome Docente'
    admin_horario_codificado.short_description = 'Horario Codificado'
    admin_quantidade_de_vagas.short_description = 'Quantidade de Vagas'
    admin_departamento.short_description = 'Departamento'

    list_display = (
        admin_nome_disciplina,
        admin_codigo_disciplina,
        admin_nome_docente,
        admin_horario_codificado,
        admin_quantidade_de_vagas,
        admin_departamento,
    )

    search_fields = [
        'nome_disciplina',
        'codigo_disciplina',
        'nome_docente',
        'horario_codificado',
    ]
