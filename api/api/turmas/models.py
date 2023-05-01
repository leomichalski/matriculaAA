from django.db import models
from model_utils.models import TimeStampedModel  # Model with created and modified columns
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from departamentos.models import Departamento


class Turma(models.Model):
    nome_disciplina = models.CharField(
        max_length=255, verbose_name='nome da disciplina'
    )
    codigo_disciplina = models.CharField(
        max_length=10, verbose_name='codigo da disciplina'
    )
    nome_docente = models.CharField(
        max_length=255, verbose_name='nome do docente'
    )
    horario_codificado = models.CharField(
        max_length=255, verbose_name='horario codificado'
    )
    quantidade_de_vagas = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)],
        verbose_name='quantidade de vagas'
    )
    departamento = models.ForeignKey(
        Departamento, related_name='turmas',
        on_delete=models.RESTRICT,
        verbose_name="departamento"
    )

    class Meta:
        ordering = ('nome_disciplina',)
        verbose_name = 'turma'
        verbose_name_plural = 'turmas'
        app_label = 'turmas'

    def __str__(self):
        return self.nome_disciplina + ' - ' + self.nome_docente + ' - ' + self.horario_codificado
