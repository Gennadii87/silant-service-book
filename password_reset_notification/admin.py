from .models import PasswordResetRequest
from django.contrib import admin, messages


@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'is_confirmed', 'user')
    list_filter = ('is_confirmed',)
    search_fields = ('email',)

    def has_add_permission(self, request):
        return False


# собственный слой для уведомления
class AdminNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if PasswordResetRequest.objects.filter(is_confirmed=False).exists():
            user = request.user
            notification_key = f'admin_notification_{user.id}'
            if not request.session.get(notification_key, False):
                messages.warning(request, "Есть запросы на сброс пароля!")
                request.session[notification_key] = True

        response = self.get_response(request)
        return response
