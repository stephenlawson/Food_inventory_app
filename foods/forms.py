from django.forms import ModelForm
from .models import Foods
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class FoodItemForm(ModelForm):
    class Meta:
        model = Foods
        fields = ['barcode', 'product_name', 'category', 'sub_category', 'location', 'quantity', 'expiration']
        widgets = {
            'expiration': DateInput(),
        }

class FoodItemFormArc(ModelForm):
    class Meta:
        model = Foods
        fields = ['quantity', 'expiration']
        widgets = {
            'expiration': DateInput(),
        }

class FoodItemFormAPI(ModelForm):
    class Meta:
        model = Foods
        fields = ['location', 'quantity', 'expiration']
        widgets = {
            'expiration': DateInput(),
        }

class FoodItemFormManual(ModelForm):
    class Meta:
        model = Foods
        fields = ['product_name', 'category', 'sub_category', 'location', 'quantity', 'expiration']
        widgets = {
            'expiration': DateInput(),
        }