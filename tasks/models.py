from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    """Задача пользователя."""

    class Priority(models.TextChoices):
        LOW = 'low', 'Низкий'
        NORMAL = 'normal', 'Обычный'
        HIGH = 'high', 'Высокий'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField('Срок выполнения', null=True, blank=True)
    priority = models.CharField(
        'Приоритет',
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )
    completed = models.BooleanField('Выполнена', default=False)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Просрочена ли невыполненная задача."""
        return (
            not self.completed
            and self.due_date is not None
            and self.due_date < timezone.now()
        )
