from django.db import models

from scraping.services import from_cyrillic_to_latin


class City(models.Model):

    name = models.CharField(
        max_length=50,
        verbose_name='город',
        unique=True,
    )
    slug = models.CharField(
        max_length=50,
        verbose_name='city',
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_latin(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):

    name = models.CharField(
        max_length=50,
        verbose_name='язык',
        unique=True,
    )
    slug = models.CharField(
        max_length=50,
        verbose_name='language',
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name = 'язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_latin(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):

    url = models.URLField(
        unique=True,
    )
    title = models.CharField(
        max_length=250,
        verbose_name='заголовок',
    )
    company = models.CharField(
        max_length=250,
        verbose_name='компания',
    )
    description = models.TextField(
        verbose_name='описание',
    )
    city = models.ForeignKey(
        'scraping.City',
        verbose_name='город',
        on_delete=models.CASCADE,
    )
    language = models.ForeignKey(
        'scraping.Language',
        verbose_name='язык',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'вакансию'
        verbose_name_plural = 'вакансии'

    def __str__(self):
        return self.title
