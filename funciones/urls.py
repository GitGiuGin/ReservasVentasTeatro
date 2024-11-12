from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import crear_funcion, actualizar_funcion, editar_funcion, eliminar_funcion

urlpatterns = [
    path('register/', crear_funcion, name='crear_funcion'),
    path('list/update/obra<int:obra_id>/funcion<int:funcion_id>', actualizar_funcion, name='actualizar_funcion'),
    path('list/editarFuncion', editar_funcion, name="funcion_editar"),
    path('list/eliminarFuncion/<int:funcion_id>', eliminar_funcion, name="funcion_eliminar"),
]