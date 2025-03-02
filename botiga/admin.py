
from django.contrib import admin
from botiga.models import (
    Usuari, Categoria, Producte, ProducteCategoria, Variant, Talla, Stock, 
    IVA, MetodeEnviament, Cistell, Item, Empresa, MetodePagament, Factura, LineaFactura
)

# 🔹 Personaliza el Admin de Usuari
@admin.register(Usuari)
class UsuariAdmin(admin.ModelAdmin):
    list_display = ('nom_usu', 'email', 'adreca_usu')  # Columnas visibles
    search_fields = ('nom_usu', 'email')  # Buscar por estos campos

# 🔹 Personaliza el Admin de Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nom_cat', 'pare')  
    list_filter = ('pare',)  # Filtrar por categorías padre
    search_fields = ('nom_cat',)  

# 🔹 Personaliza el Admin de Producte
@admin.register(Producte)
class ProducteAdmin(admin.ModelAdmin):
    list_display = ('nom_prod', 'descripcio')
    search_fields = ('nom_prod',)

# 🔹 Personaliza el Admin de Variant
@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('producte', 'color', 'preu', 'descompte')  
    list_filter = ('color', 'preu')  
    search_fields = ('color', 'producte__nom_prod')  # Permite buscar productos por nombre

# 🔹 Personaliza el Admin de Stock
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('variant', 'talla', 'quantitat')  
    list_filter = ('talla',)  

# 🔹 Personaliza el Admin de Factura
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('num_factura', 'data', 'total', 'iva_total', 'import_total')  
    list_filter = ('data', 'empresa')  
    search_fields = ('num_factura',)

# 🔹 Personaliza el Admin de MetodeEnviament
@admin.register(MetodeEnviament)
class MetodeEnviamentAdmin(admin.ModelAdmin):
    list_display = ('nom_env', 'preu_base', 'iva', 'preu_min_gratis')  
    list_filter = ('iva',)

# 🔹 Personaliza el Admin de Empresa
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nom_empresa', 'mail', 'telf')  
    search_fields = ('nom_empresa', 'mail')

# 🔹 Personaliza el Admin de Cistell
@admin.register(Cistell)
class CistellAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'data_creacio', 'metod_env')  
    list_filter = ('data_creacio',)  
# Register your models here.
