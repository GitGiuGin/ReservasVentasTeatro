# usuario/forms.py
from django import forms
from .models import Usuario  # Asegúrate de importar tu modelo de Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Usuario  # Cambia esto por el nombre real de tu modelo de cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion']  # Ajusta los campos según tu modelo
