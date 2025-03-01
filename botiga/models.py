from django.db import models

# Create your models here.
class IVA(models.Model):
    name = models.CharField(max_length=200)

class factura(models.Model):
    iva_id = models.ForeignKey(IVA, on_delete=models.CASCADE)
