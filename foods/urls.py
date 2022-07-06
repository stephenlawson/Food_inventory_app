from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create_food_item/', views.CreateFoodItem, name='create_food_item'),
    path('update_food_item/<str:pk>/', views.UpdateFoodItem, name='update_food_item'),
    path('delete_food_item/<str:pk>/', views.DeleteFoodItem, name='delete_food_item'),
    path('search_archive/', views.SearchArchive, name='search_archive'),
    path('archive_form/<str:barcode>/', views.ArchiveForm, name='archive_form'),
    path('API_form/<str:barcode>/', views.APIForm, name='API_form'),
    path('manual_form/<str:barcode>/', views.ManualForm, name='manual_form')
]