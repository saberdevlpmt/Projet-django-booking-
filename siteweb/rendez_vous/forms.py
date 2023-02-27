from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget, Select,DateInput
from django.forms import Textarea
from .models import User, Event
from django.utils import timezone
import pytz



class RegisterForm(UserCreationForm):
    nom = forms.CharField(max_length=30, required=True)
    adresse = forms.CharField(widget=forms.Textarea, required=True)
    email = forms.EmailField(required=True)
    numero_de_telephone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['nom', 'username', 'adresse', 'email', 'numero_de_telephone', 'password1', 'password2']
        
class Login(forms.Form):
        username=forms.CharField(label="prénom")
        password=forms.CharField(label="mot de passe",widget=forms.PasswordInput)  
        


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'time', 'commentaires']

        widgets = {
            'date': SelectDateWidget(
                attrs={
                    'class': 'form-control',
                },
                years=range(datetime.now().year, datetime.now().year + 2)
            ),
            'time': forms.Select(
                choices=[
                    ('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'),
                    ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'),
                    ('16:00', '16:00')
                ],
                attrs={'class': 'form-control'}
            ),
            'commentaires': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter comments'
                }
            ),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.datetime.now(pytz.utc).date():
            raise forms.ValidationError("La date ne peut pas être antérieure à aujourd'hui.")
        return date