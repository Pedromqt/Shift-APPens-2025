from django.db import models

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Cliente(models.Model):
    nome_completo = models.CharField(max_length=120)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    idade = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(150)])
    morada = models.CharField(max_length=200)
    observacoes = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.nome_completo} ({self.email})"
