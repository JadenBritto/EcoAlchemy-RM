from django.urls import path
from . import views

urlpatterns = [
    path('cases/', views.case_list, name='case_list'),
    path('cases/<int:pk>/', views.case_detail, name='case_detail'),
    path('cases/create/', views.create_case, name='create_case'),
]