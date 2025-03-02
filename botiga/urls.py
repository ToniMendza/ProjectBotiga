from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('categoria/<str:category_name>/', views.product_list, name='category_filter'),
]
