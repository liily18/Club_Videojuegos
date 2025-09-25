from django.urls import path
from .views import index, arrendar, misArriendos,devolver, agregar_observacion, lista_arriendos
from web.views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('videojuego/<int:juego_id>/arrendar/', arrendar, name='arrendar'),
    path('misarriendos/', misArriendos, name='misarriendos'),
    path('misarriendos/<int:juego_id>/devolver/', devolver, name='devolver'),
    path('arriendos/<int:arriendo_id>/comentar/', agregar_observacion, name='agregar_observacion'),
    path('arriendos/', lista_arriendos, name='lista_arriendos'),
]
