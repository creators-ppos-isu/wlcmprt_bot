from django.db import models
from species.models import Specie
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""

    middle_name = models.CharField(max_length=100, verbose_name="Отчество", blank=True)
    spacie = models.ForeignKey(
        Specie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Раса",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
