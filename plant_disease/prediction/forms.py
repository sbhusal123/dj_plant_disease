from django import forms

class PredictionForm(forms.Form):
    image = forms.ImageField()