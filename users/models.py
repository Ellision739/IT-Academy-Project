from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class Reader(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес")

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"