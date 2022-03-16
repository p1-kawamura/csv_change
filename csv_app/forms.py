from django.forms import ModelForm
from .models import Master
from django import forms

class Masterform(ModelForm):
    class Meta:
        model=Master
        fields=["jan","hinban","kataban",]



class Masterform2(forms.Form):
    hinban=forms.CharField(label="品番", widget=forms.Textarea(attrs={'cols': '5', 'rows': '1'}))