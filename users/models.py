from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    city = models.ForeignKey(
        'scraping.City',
        verbose_name='город',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    language = models.ForeignKey(
        'scraping.Language',
        verbose_name='язык программирования',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    send_email = models.BooleanField(
        default=True,
    )
    is_verified_email = models.BooleanField(
        default=False,
    )
