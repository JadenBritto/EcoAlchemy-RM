from django.urls import path
from . import views

urlpatterns = [
    path('waste/', views.waste_list, name='waste_list'),
    path('waste/<int:pk>/', views.waste_detail, name='waste_detail'),
    path('waste/create/', views.create_waste_listing, name='create_waste_listing'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('waste/<int:pk>/contact/', views.contact_waste_owner, name='contact_waste_owner'),
    path('products/<int:pk>/contact/', views.contact_product_owner, name='contact_product_owner'),
    path('waste/<int:pk>/complete/', views.complete_waste_listing, name='complete_waste_listing'),
    path('products/create/', views.create_product, name='create_product'),
    path('waste/<int:pk>/delete/', views.delete_waste_listing, name='delete_waste_listing'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
]
