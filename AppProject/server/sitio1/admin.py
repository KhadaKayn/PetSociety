from django.contrib import admin
from .models import Ingredientes, TipoMasa, Tamanos, Pizza, PizzaIngredientes, CustomUser, PedidoCliente
# Register your models here.

class IngredienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "stock", "precio", "oferta", "descuento", "imagen"]
    list_editable = ["stock"]
    search_fields = ["nombre"] #Puede ser más de uno en ambos
    list_filter = ["oferta", "descuento"]
    list_per_page = 10

class MasaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "disponible", "precio", "oferta", "descuento", "imagen"]
    list_editable = ["precio"]
    search_fields = ["nombre"] #Puede ser más de uno en ambos
    list_filter = ["oferta", "disponible"]
    list_per_page = 10

class TamanoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "disponible", "precio", "oferta", "descuento", "imagen"]
    list_editable = ["precio"]
    search_fields = ["nombre"] #Puede ser más de uno en ambos
    list_filter = ["oferta", "disponible"]
    list_per_page = 10

class PizzaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion", "tamano", "tipo_masa", "ingredientes", "precio", "imagen"]
    

admin.site.register(Ingredientes, IngredienteAdmin)
admin.site.register(TipoMasa, MasaAdmin)
admin.site.register(Tamanos, TamanoAdmin)
admin.site.register(Pizza)
admin.site.register(PizzaIngredientes)
admin.site.register(CustomUser)
admin.site.register(PedidoCliente)