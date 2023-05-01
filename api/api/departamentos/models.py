from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# populada automaticamente
class Departamento(models.Model):
    nome = models.CharField(
        max_length=255, verbose_name='nome do departamento'
    )
    index = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(255)],
        verbose_name='Posicao do departamento na pagina do sigaa de listar as turmas do semestre.'
    )
    codigo = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2000)],
        verbose_name='Codigo do departamento. Por exemplo, 673 para a faculdade do gama.'
    )

    class Meta:
        ordering = ('index',)
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
        app_label = 'departamentos'

    def __str__(self):
        return self.nome + ' - ' + str(self.codigo)
