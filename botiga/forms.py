from django import forms
from .models import Categoria, Producte

class CategoriaForm(forms.Form):
    title = forms.CharField(label="Titulo de tarea",max_length=50)
    description = forms.CharField(label="Descripcion",max_length=200)