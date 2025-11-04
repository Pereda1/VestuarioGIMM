from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from . import views  # Importa desde el mismo directorio

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('productos/consulta/', views.consulta_productos, name='consulta_productos'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/buscar/', views.buscar_productos, name='buscar_productos'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/estadisticas/', views.dashboard_estadisticas, name='api_estadisticas'),
    path('api/stock/actualizar/<int:id>/', views.actualizar_stock, name='actualizar_stock'),
]