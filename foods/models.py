from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

# Create your models here.

class Foods(models.Model):
    location_choices = (
        ('Fridge', 'Fridge'),
        ('Freezer', 'Freezer'),
        ('Cabinet', 'Cabinet')
    )

    barcode = models.CharField(max_length=200, null=True)
    product_name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    sub_category = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, choices=location_choices)
    quantity = models.IntegerField()
    expiration = models.DateField()
    Days_Left = models.IntegerField()
    updated = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Foods_archive(models.Model):
    location_choices = (
        ('Fridge', 'Fridge'),
        ('Freezer', 'Freezer'),
        ('Cabinet', 'Cabinet')
    )

    barcode = models.CharField(max_length=200, null=True)
    product_name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    sub_category = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, choices=location_choices)

    def __str__(self):
        return self.product_name