from django.urls import path
from .views import *

urlpatterns = [
    path('create/', crear_categoria, name='crear_categoria'),
    path('list/', consultar_categoria, name='lista_categoria'),
    path('list/update/<int:categoria_id>', actualizar_categoria, name='actualizar_categoria'),
]