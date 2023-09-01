# Generated by Django 4.1.8 on 2023-05-01 05:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("departamentos", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Turma",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome_disciplina", models.CharField(max_length=255, verbose_name="nome da disciplina")),
                ("codigo_disciplina", models.CharField(max_length=10, verbose_name="codigo da disciplina")),
                ("nome_docente", models.CharField(max_length=255, verbose_name="nome do docente")),
                ("horario_codificado", models.CharField(max_length=255, verbose_name="horario codificado")),
                (
                    "quantidade_de_vagas",
                    models.PositiveSmallIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1000),
                        ],
                        verbose_name="quantidade de vagas",
                    ),
                ),
                (
                    "departamento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="turmas",
                        to="departamentos.departamento",
                        verbose_name="departamento",
                    ),
                ),
            ],
            options={
                "verbose_name": "turma",
                "verbose_name_plural": "turmas",
                "ordering": ("nome_disciplina",),
            },
        ),
    ]