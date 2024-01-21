from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Mail, Event
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class MailForm(ModelForm):
    class Meta:
        model = Mail
        widgets = {
          'Subject': forms.Textarea(attrs={'rows':1.5, 'cols':38}),
          'Email': forms.Textarea(attrs={'rows':6, 'cols':40}),
        }
        fields = ('Subject', 'Email', )

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('Eventname',)
        widgets = {
            'Eventname':forms.Textarea(attrs={'rows':2, 'cols':30}),
        }
