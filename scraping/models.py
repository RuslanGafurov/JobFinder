from django.db import models

from scraping.services import from_cyrillic_to_latin


def default_urls():
    return {
        'headhunter': '',
        'super_job': '',
    }


class City(models.Model):
    """Модель городов"""

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
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_latin(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    """Модель языков программирования"""

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
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_latin(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    """Модель вакансий"""

    site = models.CharField(
        verbose_name='сайт',
        max_length=50,
    )
    title = models.CharField(
        max_length=250,
        verbose_name='должность',
    )
    company = models.CharField(
        max_length=250,
        verbose_name='компания',
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
    url = models.URLField(unique=True)
    description = models.TextField(verbose_name='описание')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.site)


class Error(models.Model):
    """Модель ошибок при сборе вакансий"""

    site = models.CharField(
        verbose_name='сайт',
        max_length=50,
    )
    city = models.CharField(
        verbose_name='город',
        max_length=50,
    )
    language = models.CharField(
        verbose_name='язык',
        max_length=50,
    )
    error = models.CharField(
        verbose_name='ошибка',
        max_length=250,
    )
    timestamp = models.DateField(
        auto_now_add=True,
        verbose_name='дата',
    )
    url = models.URLField()

    class Meta:
        verbose_name = 'ошибка'
        verbose_name_plural = 'ошибки'

    def __str__(self):
        return str(self.site)


class Url(models.Model):
    """Модель адресов для сбора вакансий"""

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
    urls = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'

    def __str__(self):
        return f'{str(self.city)} - {str(self.language)}'


class Suggestion(models.Model):
    """Модель предложений от пользователей"""

    email = models.EmailField(
        verbose_name="Адрес",
        max_length=255,
    )
    city = models.CharField(
        max_length=150,
        verbose_name='город',
    )
    language = models.CharField(
        max_length=150,
        verbose_name='язык',
    )
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'предложение'
        verbose_name_plural = 'предложения'

    def __str__(self):
        return f'Предложение от "{ str(self.email) }"'
