from django.forms import ModelForm
from .models import Master
from django import forms

class Masterform(forms.Form):
    jan=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","readonly":"readonly"}))
    hinban=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    kataban=forms.ChoiceField(
        choices=[("",""),("1","01"),("2","02"),("3","03"),("4","04"),("7","07")],     
        widget=forms.Select(attrs={"class":"form-select"})
    )
