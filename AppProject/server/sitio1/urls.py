from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('vista-administrador/', views.vista_administrador, name="vista_administrador"),
    path('menu/', views.menu, name="menu"),

    path('ingredientes', views.lista_productos, name="ingredientes"),
    path('ingresar_ingredientes', views.ingresar_productos, name="ingresar_ingredientes"),
    path('editar_ingredientes/<int:productos_id>', views.editar_productos, name='editar_ingredientes'),
    path('editar_masa/<int:productos_id>', views.editar_stock, name='editar_stock'),
    path('eliminar_ingredientes/<int:productos_id>/', views.eliminar_productos, name='eliminar_ingredientes'),
    path('tamanos', views.lista_tiposTamanos, name="tamanos"),
    path('editar_tamanos/<int:productos_id>/', views.editar_precio, name='editar_precio'),
    path('pizza', views.lista_pizza, name="pizza"),
    path('editar_pizza/<int:productos_id>/', views.editar_utilidades, name='editar_utilidades'),

    path('masa', views.lista_tiposMasa, name="masa"),
    path('ingresar_masa', views.ingresar_masa, name="ingresar_masa"),
    path('editar_masa/<int:masa_id>/', views.editar_masa, name='editar_masa'),
    path('eliminar_masa/<int:masa_id>/', views.eliminar_masa, name='eliminar_masa'),
    
    
    path('ingresar_tamanos', views.ingresar_tamano, name="ingresar_tamanos"),
    path('editar_tamanos/<int:tamanos_id>/', views.editar_tamano, name='editar_tamanos'),
    path('eliminar_tamanos/<int:tamanos_id>/', views.eliminar_tamano, name='eliminar_tamanos'),

    
    path('ingresar_pizza', views.ingresar_pizza, name="ingresar_pizza"),
    path('editar_pizza/<int:pizza_id>/', views.editar_pizza, name='editar_pizza'),
    path('eliminar_pizza/<int:pizza_id>/', views.eliminar_pizza, name='eliminar_pizza'),

    path('detalle_pizza/<int:pizza_id>/', views.detalle_pizza, name='detalle_pizza'),

    path('registro/', views.registro, name="registro"),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),

]
