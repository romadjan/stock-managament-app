from django import forms
from django.forms import ModelForm
from .models import *


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["category", "item_name", "quantity"]