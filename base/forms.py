from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'
        
class RegisterCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']
        
        

