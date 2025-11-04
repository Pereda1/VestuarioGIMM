from django.contrib import admin
from .models import Usrs, Productos

@admin.register(Usrs)
class UsrsAdmin(admin.ModelAdmin):
    list_display = ['IdLogin', 'Nombre', 'Rol', 'Area', 'Status']
    list_filter = ['Rol', 'Status', 'Area']
    search_fields = ['IdLogin', 'Nombre']

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ['CODIGO', 'ARTICULO', 'DISPVEST', 'DISPMAQ', 'DISPLAV', 'Estatus']
    list_filter = ['Estatus', 'MARCA']
    search_fields = ['CODIGO', 'ARTICULO', 'DESCRIP']
    list_per_page = 20