from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import consultar_obras, crear_obra, actualizar_obra, detalle_obra, cambiar_estado

urlpatterns = [
    path('list/', consultar_obras, name='lista_obra'),
    path('register/', crear_obra, name='crear_obra'),
    path('list/update/<int:id>', actualizar_obra, name='actualizar_obra'),
    path('list/obra_detalle/<int:id>', detalle_obra, name='detalle_obra'),
    path('cambiar_estado/<int:obra_id>', cambiar_estado, name='cambiar_estado'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)