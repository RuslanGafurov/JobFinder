from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    """Переопределение стандартного менеджера"""

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """Переопределение стандартной модели"""

    email = models.EmailField(
        verbose_name="Адрес",
        max_length=255,
        unique=True,
    )
    city = models.ForeignKey(
        'scraping.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    language = models.ForeignKey(
        'scraping.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    send_email = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
