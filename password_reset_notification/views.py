from django.shortcuts import render
from django.contrib.auth.models import User


from .forms import PasswordResetForm
from .models import PasswordResetRequest

from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny


def reset_password(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                form.save_request(user=user)
                success_message = 'Запрос на сброс пароля отправлен'
            else:
                error_message = 'Пользователь с указанным email не найден.'
    else:
        form = PasswordResetForm()
    return render(request, 'account/password_reset.html',
                  {'form': form, 'error_message': error_message, 'success_message': success_message})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_api(request):
    """
    {
        "email": "user@example.com"
    }
    """
    error_message = None
    success_message = None
    form = PasswordResetForm(request.data)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            form.save_request(user=user)
            PasswordResetRequest.objects.create(user=user)
            success_message = 'Запрос на сброс пароля отправлен'
        else:
            error_message = 'Пользователь с указанным email не найден.'
    else:
        error_message = 'Неверные данные для сброса пароля.'
    return Response({'error_message': error_message, 'success_message': success_message}, status=status.HTTP_200_OK)
