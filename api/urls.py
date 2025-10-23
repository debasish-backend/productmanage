from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create/', views.createItem, name='create-item'),
    path('view/', views.view_items, name='view-items'),
    path('update/<int:pk>/', views.update_item, name='update-item'),
    path('delete/<int:pk>/', views.delete_item, name='delete-item'),
]