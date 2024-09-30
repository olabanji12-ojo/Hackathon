from django import forms
from .models import Submission
from django.contrib.auth.forms import UserCreationForm
from .models import User




class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['details']
        
class RegisterCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']
        