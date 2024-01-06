from django import forms
from users.models import Users

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'role', 'image']