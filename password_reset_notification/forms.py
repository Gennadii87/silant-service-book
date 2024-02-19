from django import forms
from .models import *


class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def save_request(self, user=None):
        email = self.cleaned_data['email']
        if user is None:
            user = User.objects.filter(email=email).first()

        password_reset_request = PasswordResetRequest.objects.create(user=user, email=email)
        return password_reset_request
