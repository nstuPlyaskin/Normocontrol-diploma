from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CheckOut(models.Model):
    student = models.ForeignKey(
        User,
        verbose_name='Студент',
        help_text='Выберите студента из списка',
        on_delete=models.CASCADE,
        related_name='checkout_student',
    )
    check_date = models.DateTimeField(
        verbose_name='Дата проверки',
        help_text='Укажите дату проверки',
        auto_now_add=True,
        db_index=True,
    )
    info = models.TextField(
        verbose_name='Сопроводительная информация',
        help_text='При необходимости укажите дополнительные сведения',
        max_length=1000,
        null=True,
        blank=True,
    )
    status = models.BooleanField(
        default=False,
        verbose_name='Текущий статус проверки работы',
        help_text='Укажите текущий статус проверки',
        null=True,
    )
    docx_file = models.FileField(
        verbose_name='Дипломная работа (расширение docx)',
        help_text='Укажите файл с расширением docx, размером не более 8 Мб',
        upload_to='diplomas/%Y/%m/%d/',
        null=True,
    )
    pdf_file = models.FileField(
        verbose_name='Дипломная работа (расширение pdf)',
        help_text='Укажите файл с расширением pdf, размером не более 8 Мб',
        upload_to='diplomas/%Y/%m/%d/',
        null=True,
    )

    def __str__(self):
        return f'check_{self.id}'

    class Meta:
        ordering = ['check_date']


class Remark(models.Model):
    section = models.CharField(
        verbose_name='Раздел ПЗ страницы',
        help_text='Укажите раздел ПЗ',
        max_length=100,
    )
    page_number = models.CharField(
        verbose_name='Номер страницы',
        help_text='Укажите номер страницы',
        null=True,
        blank=True,
        max_length=100,
    )
    paragraph = models.CharField(
        verbose_name='Номер абзаца',
        help_text='Укажите номер абзаца',
        null=True,
        blank=True,
        max_length=100,
    )
    check_all = models.CharField(
        verbose_name='Проверить замечания по всему документу',
        help_text='Уточните необходимость проверки по всему документу',
        max_length=100,
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текст замечания',
        help_text='Введите текст замечания',
        max_length=300,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор замечания',
        help_text='Укажите автора замечания',
        on_delete=models.CASCADE,
        related_name='remark'
    )
    check_out = models.ForeignKey(
        CheckOut,
        on_delete=models.CASCADE,
        related_name='remark',
    )
    check_date = models.DateTimeField(
        verbose_name='Дата публикации замечания',
        help_text='Укажите дату публикации замечания',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return f'remark_{self.id}'

    class Meta:
        ordering = ['check_date']
