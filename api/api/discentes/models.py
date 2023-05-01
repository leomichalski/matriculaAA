from django.db import models
from model_utils.models import TimeStampedModel  # Model with created and modified columns
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from turmas.models import Turma


class Discente(TimeStampedModel):
    turmas_desejadas = models.ManyToManyField(
        Turma, related_name='discentes_interessados',
        verbose_name='turmas desejadas'
    )
    # TODO: validar matricula
    matricula = models.IntegerField(
        # validators=[MatriculaValidator()],
        verbose_name='matricula'
    )
    # Nao eh uma forma segura de armazenar as senhas.
    # Em compensacao, as senhas sao armazenadas durante somente 1 semana.
    # Dps dessa semana, eh recomendado que os usuarios redefinam suas senhas.
    senha = models.CharField(
        max_length=100, verbose_name='senha'
    )
    # TODO: validar CPF
    cpf = models.BigIntegerField(
        # validators=[CPFValidator()],
        unique=True, verbose_name='CPF'
    )
    data_de_nascimento = models.DateField(
        verbose_name='data de nascimento'
    )
    email = models.EmailField(
        unique=True, max_length=254, verbose_name='email'
    )

    class Meta:
        ordering = ('email',)
        verbose_name = 'discente'
        verbose_name_plural = 'discentes'
        app_label = 'discentes'

    def __str__(self):
        return self.email
