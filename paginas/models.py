from django.db import models


# Create your models here.
class RelatorioModel(models.Model):
    MESES_CHOICES = (
        (1, "Janeiro"),
        (2, "Fevereiro"),
        (3, "Março"),
        (4, "Abril"),
        (5, "Maio"),
        (6, "Junho"),
        (7, "Julho"),
        (8, "Agosto"),
        (9, "Setembro"),
        (10, "Outubro"),
        (11, "Novembro"),
        (12, "Dezembro"),
    )

    STATUS_CHOICES = (
        (1, 'Aberto'),
        (2, 'Fechado'),

    )

    dataLimite = models.DateField()
    mes = models.IntegerField(unique=True, choices=MESES_CHOICES, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False)
