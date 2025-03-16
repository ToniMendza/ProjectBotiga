from django.shortcuts import render, get_object_or_404,redirect
from .models import *

def get_descendant_categories(category):
    descendants = []
    children = Categoria.objects.filter(pare=category)
    for child in children:
        descendants.append(child)
        descendants.extend(get_descendant_categories(child))
    return descendants

def get_ancestor_categories(category):
    ancestors = []
    while category:
        ancestors.insert(0, category)
        category = category.pare
    return ancestors


def product_list(request, category_id=None, product_id=None, variant_id=None,talla_id=None):
    categories = Categoria.objects.filter(pare__isnull=True)
    products = Producte.objects.prefetch_related("variant_set")

    # categories_with_subs = {category: list(category.categoria_set.all()) for category in categories}

    # products = Producte.objects.filter(
    #     variant__stock__quantitat__gt=0
    # ).distinct().prefetch_related("variant_set")


    selected_category = None
    catAcumulades = []
    subcategories = []
    talles = Talla.objects.all()

    # 🔹 Si el usuario quiere limpiar filtros
    if "clear_filters" in request.GET:
        request.session.clear()
        return redirect("home")    

    # 🔹 FILTROS: Guardar en session cuando sea POST
    if request.method == "POST":
        if "nom" in request.POST:
            request.session["nom_filter"] = request.POST.get("nom", "")
        if "min" in request.POST and "max" in request.POST:
            request.session["min_price"] = request.POST.get("min", "")
            request.session["max_price"] = request.POST.get("max", "")
        if "talla" in request.POST:
            request.session["size_filter"] = request.POST.getlist("talla")

    # 🔹 Obtener valores de session para aplicar filtros
    name_query = request.session.get("nom_filter", "")
    min_price = request.session.get("min_price", "")
    max_price = request.session.get("max_price", "")
    selected_sizes = Talla.objects.filter(n_talla__in=request.session.get("size_filter", []))


    if category_id:
        selected_category = get_object_or_404(Categoria, id=category_id)
        catAcumulades = get_ancestor_categories(selected_category)
        subcategories = Categoria.objects.filter(pare=selected_category)

        descendant_categories = [selected_category] + get_descendant_categories(selected_category)
    #    recuperamos los productos de la categoría seleccionada y sus descendientes
        products = Producte.objects.filter(categories__in=descendant_categories).distinct().prefetch_related('variant_set')


    # 🔹 Aplicar Filtros
    if name_query:
        products = products.filter(nom_prod__icontains=name_query)

    # Filtrado por precio en las variantes
    if min_price:
        # Filtrar por precio de las variantes relacionadas
        products = products.filter(variant__preu__gte=min_price)

    if max_price:
        # Filtrar por precio de las variantes relacionadas
        products = products.filter(variant__preu__lte=max_price)

    # Filtrado por talla (es necesario que esté relacionada correctamente con Variant en Stock)
    if selected_sizes:
        # Filtrar productos según las tallas seleccionadas
        products = products.filter(variant__stock__talla__in=selected_sizes).distinct()

    # if product_id:
    #     product = get_object_or_404(Producte, id=product_id)
    #     variants = product.variant_set.all()
    #     if variant_id:
    #         variant = get_object_or_404(variants, id=variant_id)
    #         stocks = variant.stock_set.all()
    #         if talla_id:
    #             stock = get_object_or_404(stocks, talla_id=talla_id)
    #     return redirect("home")    

    return render(request, 'index.html', {
        'categories': categories,
        'selected_category': selected_category,
        'catAcumulades': catAcumulades,
        'subcategories': subcategories,
        'products': products,
        'name_query': name_query,
        'min_price': min_price,
        'max_price': max_price,
        'selected_sizes': selected_sizes,
        'talles': talles,
        # 'categories_with_subs': categories_with_subs
    })

def product_detall(request, variant_id):
    # 🔹 Obtener la variante seleccionada directamente
    selected_variant = get_object_or_404(Variant, id=variant_id)

    # 🔹 Obtener el producto relacionado
    product = selected_variant.producte

    # 🔹 Obtener la categoría del producto
    selected_category = product.categories.first()
    catAcumulades = get_ancestor_categories(selected_category) if selected_category else []

    # 🔹 Obtener todas las variantes del producto
    variants = product.variant_set.all()

    # 🔹 Obtener las imágenes de la variante seleccionada
    imatges = selected_variant.imatges.all()

    # 🔹 Obtener stock disponible de la variante seleccionada
    stocks = selected_variant.stock_set.all()

    return render(request, 'product_detail.html', {
        'selected_variant': selected_variant,  # 🔹 Pasamos la variante directamente
        'product': product,  # 🔹 Para mostrar nombre, descripción, etc.
        'variants': variants,  # 🔹 Para cambiar entre variantes
        'stocks': stocks,  # 🔹 Para mostrar tallas disponibles
        'selected_category': selected_category,  # 🔹 Para breadcrumbs
        'catAcumulades': catAcumulades,  # 🔹 Para mostrar ruta de categorías
        'imatges': imatges  # 🔹 Para mostrar imágenes de la variante seleccionada
    })

def afegir_a_cistell(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        quantitat = int(request.POST.get('quantitat', 1))
        stock = get_object_or_404(Stock, id=stock_id)

        # 🔍 Buscar cistell actiu de l'usuari o crear-lo
        cistell, created = Cistell.objects.get_or_create(usuari=request.user.usuari, metod_env_id=1)  # ⚠️ Ajusta ID metode enviament

        # 🔄 Buscar si ja hi ha aquest ítem i sumar quantitat
        item, item_created = Item.objects.get_or_create(cistell=cistell, stock=stock)
        if item_created:
            item.quantitat = quantitat
        else:
            item.quantitat += quantitat
        item.save()

        # ✅ Redirigeix al detall del producte
        return redirect('product_detall', variant_id=stock.variant.id)
