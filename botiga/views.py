from django.shortcuts import render
from .models import Categoria, Producte, ProducteCategoria

def product_list(request, category_name=None):
    categories = Categoria.objects.filter(pare__isnull=True)  # Solo categorías principales
    products = Producte.objects.all()  # Mostrar todos los productos por defecto

    if category_name:
        try:
            category = Categoria.objects.get(nom_cat=category_name)
            product_ids = ProducteCategoria.objects.filter(id_categoria=category).values_list('id_producte', flat=True)
            products = Producte.objects.filter(id__in=product_ids)
        except Categoria.DoesNotExist:
            products = []  # Si la categoría no existe, no mostrar productos

    return render(request, 'index.html', {
        'categories': categories,
        'products': products
    })
