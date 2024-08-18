from django.db import models


class Specie(models.Model):
    """Модель расы"""

    title = models.CharField(max_length=100)
    description = models.TextField("Описание")
    participants_count = models.PositiveIntegerField(
        "Оставшееся число участников", default=20
    )

    class Meta:
        verbose_name = "Раса"
        verbose_name_plural = "Расы"

    def __str__(self):
        return self.title
