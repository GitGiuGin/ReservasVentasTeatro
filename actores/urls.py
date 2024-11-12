from django.urls import path
from django.contrib.auth import views as auth_views
from .views import consultar_actor, crear_actor, actualizar_actor

urlpatterns = [
    path('list/', consultar_actor, name='lista_actor'),
    path('register/', crear_actor, name='crear_actor'),
    path('list/update/<int:id>', actualizar_actor, name='actualizar_actor'),
]