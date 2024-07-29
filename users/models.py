from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify


class Group(models.Model):
    title = models.CharField(
        verbose_name='Название группы',
        help_text='Введите название группы',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Slug-метка',
        help_text='Укажите адрес для страницы группы',
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Укажите электронную почту',
        null=True,
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        help_text='Выберите группу из списка',
        on_delete=models.SET_NULL,
        related_name='user',
        null=True,
    )
    allow_manage = models.BooleanField(
        default=False,
        verbose_name='Доступ к управлению',
        help_text='Открывает пользователю функционал проверки работ',
        null=True,
    )

    def __str__(self):
        return self.username
