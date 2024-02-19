from django.urls import path
from .views import reset_password, reset_password_api


urlpatterns = [
    path('api/reset_password/', reset_password_api, name='reset_password_api'),
    path('request/', reset_password, name='reset_password_view'),
]
