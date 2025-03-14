from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('categoria/<int:category_id>/', views.product_list, name='category_filter'),
    path('producte/<int:product_id>/', views.product_detall, name='product_detail'),
    path('producte/<int:product_id>/variant/<int:variant_id>/', views.product_detall, name='product_detail_variant'),

]

if settings.DEBUG:  # Solo en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)