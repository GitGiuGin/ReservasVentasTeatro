from django.urls import path
from django.contrib.auth import views as auth_views
from .views import consultar_clientes, crear_cliente, actualizar_cliente, custom_login_view, registro_cliente_desde_login, clientesForm, mis_reservas

urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('list/', consultar_clientes, name='lista_cliente'),
    path('register/', clientesForm, name='nuevo_cliente'),
    path('registrarCliente/', crear_cliente, name='crear_cliente'),
    path('registrarDesdeLogin/', registro_cliente_desde_login, name='cliente_registrar_login'),
    path('list/update/<int:id>', actualizar_cliente, name='actualizar_cliente'),
    path('listaReservas/', mis_reservas, name='mis_reservas'),
]