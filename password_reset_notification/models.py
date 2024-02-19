from django.db import models
from django.contrib.auth.models import User


class PasswordResetRequest(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    email = models.EmailField(verbose_name='email пользователя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтверждение')

    def __str__(self):
        return f"Запросы пользователей {self.user}"

    class Meta:
        verbose_name = 'Запрос от пользователя на сброс'
        verbose_name_plural = 'Запросы от пользователей на сброс'
