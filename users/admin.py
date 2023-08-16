from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Расширенное отображение модели пользователя"""

    list_display = ('username', 'city', 'language', 'send_email')
