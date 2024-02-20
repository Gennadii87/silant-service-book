from django.apps import AppConfig


class PasswordResetNotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'password_reset_notification'
    verbose_name = 'Запросы пользователей'
