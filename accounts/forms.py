from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

from django import forms

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=(('REPORTER', 'Reporter'), ('COLLECTOR', 'Collector')))
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.role == 'COLLECTOR':
            user.status = 'PENDING'
        else:
            user.status = 'APPROVED'
        if commit:
            user.save()
        return user
