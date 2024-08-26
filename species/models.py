from django.db import models


class Specie(models.Model):
    """Модель антилокации"""

    title = models.CharField(max_length=100)
    description = models.TextField("Описание")
    participants_left = models.PositiveIntegerField(
        "Оставшееся число участников", default=20
    )

    class Meta:
        verbose_name = "Антилокация"
        verbose_name_plural = "Антилокации"

    def __str__(self):
        return self.title
    

class SpeciePhoto(models.Model):
    """Модель фотографии антилокации"""

    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    photo = models.ImageField("Фото", upload_to="species/", null=True, blank=True)

    class Meta:
        verbose_name = "Фотография антилокации"
        verbose_name_plural = "Фотографии антилокации"