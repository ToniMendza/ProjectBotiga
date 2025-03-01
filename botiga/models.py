from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import re
from django.core.exceptions import ValidationError

def validate_email(value):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, value):
        raise ValidationError("El email no es valid")

class Usuari(models.Model):
    nom_usu = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, unique=True, validators=[validate_email])
    contrasenya = models.CharField(max_length=255, null=False)
    adreca_usu = models.TextField(null=True)

class Categoria(models.Model):
    nom_cat = models.CharField(max_length=100, null=False)
    pare = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

class Producte(models.Model):
    nom_prod = models.CharField(max_length=150, null=False)
    descripcio = models.TextField(null=False)

class ProducteCategoria(models.Model):
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_producte = models.ForeignKey(Producte, on_delete=models.CASCADE)

class Variant(models.Model):
    color = models.CharField(max_length=50, null=False)
    preu = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    descompte = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE)
    imatge = models.CharField(max_length=100, null=False)

class Talla(models.Model):
    n_talla = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)])

class Stock(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    quantitat = models.IntegerField(validators=[MinValueValidator(0)])

class IVA(models.Model):
    percentatge = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])

class MetodeEnviament(models.Model):
    nom_env = models.CharField(max_length=50, null=False)
    preu_base = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    iva = models.ForeignKey(IVA, on_delete=models.CASCADE)
    preu_min_gratis = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])

class Cistell(models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    data_creacio = models.DateTimeField(auto_now_add=True)
    metod_env = models.ForeignKey(MetodeEnviament,on_delete=models.CASCADE)

class Item(models.Model):
    quantitat = models.IntegerField(validators=[MinValueValidator(1)])
    cistell = models.ForeignKey(Cistell, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

class Empresa(models.Model):
    nom_empresa = models.CharField(max_length=255, null=False)
    mail = models.EmailField(max_length=100, unique=True)
    telf = models.CharField(max_length=20, null=False)
    img_logo = models.TextField(null=False)
    adreca_empresa = models.TextField(null=False)

class MetodePagament(models.Model):
    nom_metode = models.CharField(max_length=50, null=False)
    descripcio = models.TextField(null=False)

class Factura(models.Model):
    cistell = models.ForeignKey(Cistell, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    data = models.DateField(null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    iva_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    import_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    num_factura = models.IntegerField(null=False)
    any = models.IntegerField(null=False)
    base_imposable = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    enviu = models.ForeignKey(MetodeEnviament, on_delete=models.CASCADE)
    met_pagament = models.ForeignKey(MetodePagament, on_delete=models.SET_NULL, null=True)

class LineaFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    iva = models.ForeignKey(IVA, on_delete=models.CASCADE)
    quantitat = models.IntegerField(validators=[MinValueValidator(1)])
    preu_base = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    iva_percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    descompte = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
