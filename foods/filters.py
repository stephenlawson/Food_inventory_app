import django_filters
from django.forms.widgets import TextInput, Select, NumberInput
from django_filters import CharFilter, ChoiceFilter, NumberFilter, DateFilter

from .models import *

location_choices = (
        ('Fridge', 'Fridge'),
        ('Freezer', 'Freezer'),
        ('Cabinet', 'Cabinet')
    )

class FoodFilter(django_filters.FilterSet):
    barcode=CharFilter(field_name='barcode', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 50,}))
    product_name=CharFilter(field_name='product_name', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 50,}))
    category=CharFilter(field_name='category', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 50,}))
    sub_category=CharFilter(field_name='sub_category', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 50,}))
    location=ChoiceFilter(field_name='location', label="",choices=location_choices, widget=Select(attrs={ 'class': 'form-control',
            'width': 50,}))
    quantity=NumberFilter(field_name='quantity', lookup_expr="lte", label="", widget=NumberInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 50,}))
    expiration=CharFilter(field_name='expiration', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 50,}))
    updated=CharFilter(field_name='updated', lookup_expr='icontains', label="", widget=TextInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 50,}))
    Days_Left=NumberFilter(field_name='Days_Left', lookup_expr="lte", label="", widget=NumberInput(attrs={'placeholder': 'Filter', 'class': 'form-control',
            'size': 100,}))    

    start_date = DateFilter(field_name="expiration", lookup_expr='gte')
    start_date = DateFilter(field_name="expiration", lookup_expr='lte')
    class Meta:
        model = Foods
        fields = ['barcode', 'product_name', 'category', 'sub_category', 'location', 'quantity', 'expiration', 'Days_Left']