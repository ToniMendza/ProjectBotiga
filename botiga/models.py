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
    adreca_usu = models.CharField(max_length=255, null=True)