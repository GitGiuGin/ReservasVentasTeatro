from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('user/', include('usuario.urls')),
    path('reservas/', include('reserva.urls')),
    path('obras/', include('obra.urls')),
    path('asiento/', include('asiento.urls')),
    path('actores/', include('actores.urls')),
    #path('pagos/', include('pago.urls')),
    path('funciones/', include('funciones.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
