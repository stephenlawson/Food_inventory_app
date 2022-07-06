from django.contrib import admin

# Register your models here.

from .models import Foods, Foods_archive

admin.site.register(Foods)
admin.site.register(Foods_archive)