from django.db import models

from scraping.services import from_cyrillic_to_latin


def default_urls():
    return {
        'headhunter': '',
    }


class City(models.Model):
    """Города"""

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
    """Языки программирования"""

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
    """Вакансии"""

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
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    """Ошибки при сборе вакансий"""

    data = models.JSONField()
    timestamp = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'ошибка'
        verbose_name_plural = 'ошибки'

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    """Адреса для сбора вакансий"""

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
    urls_data = models.JSONField(
        default=default_urls,
    )

    class Meta:
        unique_together = ('city', 'language')
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'

    def __str__(self):
        return f'{str(self.city)} - {str(self.language)}'


class Suggestion(models.Model):
    """Предложения пользователей"""

    email = models.EmailField(
        verbose_name="Адрес",
        max_length=255,
        unique=True,
    )
    city = models.CharField(
        max_length=150,
        verbose_name='город',
    )
    language = models.CharField(
        max_length=150,
        verbose_name='язык',
    )
    timestamp = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'предложение'
        verbose_name_plural = 'предложения'

    def __str__(self):
        return f'От "{ str(self.email) }": { str(self.timestamp) }'
