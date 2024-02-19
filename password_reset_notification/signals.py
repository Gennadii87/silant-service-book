from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import PasswordResetRequest


@receiver(post_save, sender=PasswordResetRequest)
def handle_password_reset_request(sender, instance, created, **kwargs):
    if created:
        # Отправляем email
        subject = 'Сброс пароля'
        message = render_to_string('reset_password_email.txt', {
            'reset_request': instance,
            'user': instance.user,
        })
        from_email = 'webmaster@localhost'  # Замените на свой email
        to_email = [instance.email]
        send_mail(subject, message, from_email, to_email)
