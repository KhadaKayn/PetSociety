from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from sitio1.models import Ingredientes, TipoMasa, Tamanos, Pizza, Productos
from .forms import TipoMasaForm, TamanosForm, IngredientesForm, ProductosForm, PizzaForm, CustomUserCreationForm, StockOptimoForm, PrecioOptimoForm, UtilidadesForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product


def recalcular_precios_pizzas(ingrediente):
    pizzas = ingrediente.pizza_set.all()

    for pizza in pizzas:
        pizza.precio = pizza.calcular_precio()
        pizza.save()

def recalcular_precios_pizzas(masa):
    pizzas = masa.pizza_set.all()

    for pizza in pizzas:
        pizza.precio = pizza.calcular_precio()
        pizza.save()

def recalcular_precios_pizzas(tamano):
    pizzas = tamano.pizza_set.all()

    for pizza in pizzas:
        pizza.precio = pizza.calcular_precio()
        pizza.save()



#                                                       PAGINA DE INICIO
def home(request):
    productos = Productos.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'sitio1/home.html', data)


#                                                       MENÚ
def menu(request):
    productos = Productos.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'sitio1/menu.html', data)

#                                                       ADMIN
@permission_required('sitio1.view_tipomasa')
def vista_administrador(request):
    return render(request, 'sitio1/vista_administrador.html')

#                                                       VISTAS // INGREDIENTES

            #listado
def lista_productos(request):
    listaProductos = Productos.objects.all()
    return render(request, 'sitio1/DataModelApp/ingredientes/ver_ingredientes.html',{"datos":listaProductos})

def lista_ingredientes(request):
    listaIngredientes = Ingredientes.objects.all()
    return render(request, 'sitio1/DataModelApp/ingredientes/ver_ingredientes.html',{"datos":listaIngredientes})

            #ingreso
@permission_required('sitio1.add_ingredientes')
def ingresar_productos(request):
    if request.method == "POST":
        form = ProductosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect("ingredientes")
    else:
        form = ProductosForm()

    return render(request, 'sitio1/DataModelApp/ingredientes/ingresar_ingredientes.html', {'form': form})
    
@permission_required('sitio1.change_pizza')
def editar_productos(request, productos_id):
    producto = get_object_or_404(Productos, pk=productos_id)

    if request.method == 'POST':
        form = ProductosForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("ingredientes")
    else:
        form = ProductosForm(instance=producto)

    return render(request, 'sitio1/DataModelApp/ingredientes/editar_ingredientes.html', {'form': form})

def editar_utilidades(request, productos_id):
    producto = get_object_or_404(Productos, pk=productos_id)

    if request.method == 'POST':
        form = UtilidadesForm(request.POST, instance=producto)
        if form.is_valid():
            utilidad_mes1, utilidad_mes2 = form.calcular_utilidades()

            # Guardar siempre la utilidad actual y anterior
            producto.utilidades_anteriores = utilidad_mes1
            producto.utilidades_actuales = utilidad_mes2

            if utilidad_mes2 > utilidad_mes1:
                producto.precio = form.cleaned_data['precio_mes2']
                producto.promedio_ventas_dia = form.cleaned_data['promedio_ventas_dia_mes2']
                messages.success(request, '¡Utilidad aumentada con éxito!')
            else:
                messages.warning(request, '¡Alerta! La utilidad ha disminuido.')

            producto.save()
            return redirect("pizza")
    else:
        form = UtilidadesForm(instance=producto)

    return render(request, 'sitio1/DataModelApp/pizzas/editar_pizza.html', {'form': form})

def editar_precio(request, productos_id):
    producto = get_object_or_404(Productos, pk=productos_id)

    if request.method == 'POST':
        form = PrecioOptimoForm(request.POST, instance=producto)
        if form.is_valid():
            precio_optimo = form.calcular_precio_optimo()
            producto.precio = precio_optimo
            producto.save()
            return redirect("tamanos")
    else:
        form = PrecioOptimoForm(instance=producto)

    return render(request, 'sitio1/DataModelApp/tipos_tamano/editar_tamanos.html', {'form': form})

def editar_stock(request, productos_id):
    producto = get_object_or_404(Productos, pk=productos_id)

    if request.method == 'POST':
        form = StockOptimoForm(request.POST, instance=producto)
        if form.is_valid():
            # Obtener los valores de los campos adicionales
            tiempo_entrega_dias = form.cleaned_data['tiempo_entrega_dias']
            stock_seguridad = form.cleaned_data['stock_seguridad']
            promedio_ventas_dia = form.cleaned_data['promedio_ventas_dia']
            
            # Calcular el stock óptimo
            demanda_durante_tiempo_entrega = promedio_ventas_dia * tiempo_entrega_dias
            stock_optimo = demanda_durante_tiempo_entrega + stock_seguridad
            
            # Guardar el stock óptimo en el modelo
            producto.stock_optimo = stock_optimo
            producto.save()
            return redirect("masa")
    else:
        form = StockOptimoForm(instance=producto)

    return render(request, 'sitio1/DataModelApp/tipos_masa/editar_masa.html', {'form': form})

@permission_required('sitio1.delete_pizza')
def eliminar_productos(request, productos_id):
    producto = Productos.objects.get(pk=productos_id)
    producto.delete()
    return redirect("ingredientes")

@permission_required('sitio1.add_ingredientes')
def ingresar_ingredientes(request):
    if request.method == "POST":
        form = IngredientesForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect("ingredientes")
    else:
        form = IngredientesForm()

    return render(request, 'sitio1/DataModelApp/ingredientes/ingresar_ingredientes.html', {'form': form})
    
            #modificar
@permission_required('sitio1.change_ingredientes')
def editar_ingredientes(request, ingredientes_id):
    ingrediente = get_object_or_404(Ingredientes, pk=ingredientes_id)

    if request.method == "POST":
        form = IngredientesForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            recalcular_precios_pizzas(ingrediente)
            return redirect("/sitio1/ingredientes")
    else:
        form = IngredientesForm(instance=ingrediente)   
    
    return render(request, 'sitio1/DataModelApp/ingredientes/editar_ingredientes.html', {"form": form})
    
            #eliminar
@permission_required('sitio1.delete_ingredientes')
def eliminar_ingredientes(request, ingrediente_id):
    ingrediente = Ingredientes.objects.get(pk=ingrediente_id)
    ingrediente.delete()
    return redirect("/sitio1/ingredientes")

#                                                       VISTAS // Tipos De Masa

            #listado
def lista_tiposMasa(request):
    productos = Productos.objects.all()
    return render(request, 'sitio1/DataModelApp/tipos_masa/ver_masa.html',{"datos":productos})

            #ingreso
@permission_required('sitio1.add_tipomasa')
def ingresar_masa(request):
    if request.method == 'POST':
        form = TipoMasaForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect("masa")
    else:
        form = TipoMasaForm()

    return render(request, 'sitio1/DataModelApp/tipos_masa/ingresar_masa.html', {'form': form})
    
            #modificar
@permission_required('sitio1.change_tipomasa')
def editar_masa(request, masa_id):
    masa = get_object_or_404(TipoMasa, pk=masa_id)

    if request.method == 'POST':
        form = TipoMasaForm(request.POST, instance=masa)
        if form.is_valid():
            form.save()
            recalcular_precios_pizzas(masa)
            return redirect("/sitio1/masa")
    else:
        form = TipoMasaForm(instance=masa)

    return render(request, 'sitio1/DataModelApp/tipos_masa/editar_masa.html', {'form': form})
    
            #eliminar
@permission_required('sitio1.delete_tipomasa')
def eliminar_masa(request, masa_id):
    masa = TipoMasa.objects.get(pk=masa_id)
    masa.delete()
    return redirect("/sitio1/masa")

#                                                       VISTAS // Tipos De Tamaño

            #listado
def lista_tiposTamanos(request):
    listaTamanos = Productos.objects.all()
    return render(request, 'sitio1/DataModelApp/tipos_tamano/ver_tamanos.html',{"datos":listaTamanos})

            #ingreso
@permission_required('sitio1.add_tamanos')
def ingresar_tamano(request):
    if request.method == 'POST':
        form = TamanosForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect("/sitio1/tamanos")
    else:
        form = TamanosForm()

    return render(request, 'sitio1/DataModelApp/tipos_tamano/ingresar_tamanos.html', {'form': form})

            #modificar   
@permission_required('sitio1.change_tamanos') 
def editar_tamano(request, tamanos_id):
    tamano = get_object_or_404(Tamanos, pk=tamanos_id)

    if request.method == 'POST':
        form = TamanosForm(request.POST, instance=tamano)
        if form.is_valid():
            form.save()
            recalcular_precios_pizzas(tamano)
            return redirect("/sitio1/tamanos")
    else:
        form = TipoMasaForm(instance=tamano)

    return render(request, 'sitio1/DataModelApp/tipos_tamano/editar_tamanos.html', {'form': form})

            #eliminar  
@permission_required('sitio1.delete_tamanos')  
def eliminar_tamano(request, tamanos_id):
    tamano = Tamanos.objects.get(pk=tamanos_id)
    tamano.delete()
    return redirect("/sitio1/tamanos")

#                                                       VISTAS // Pizzas

            #listado
def lista_pizza(request):
    listaPizzas = Productos.objects.all()
    return render(request, 'sitio1/DataModelApp/pizzas/ver_pizzas.html',{"datos":listaPizzas})

            #ingreso
@permission_required('sitio1.add_pizza')
def ingresar_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect("/sitio1/pizza")
    else:
        form = PizzaForm()

    return render(request, 'sitio1/DataModelApp/pizzas/ingresar_pizza.html', {'form': form})

            #modificar    
@permission_required('sitio1.change_pizza')
def editar_pizza(request, pizza_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)

    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            form.save()
            return redirect("/sitio1/pizza")
    else:
        form = PizzaForm(instance=pizza)

    return render(request, 'sitio1/DataModelApp/pizzas/editar_pizza.html', {'form': form})

            #eliminar    
@permission_required('sitio1.delete_pizza')
def eliminar_pizza(request, pizza_id):
    pizza = Pizza.objects.get(pk=pizza_id)
    pizza.delete()
    return redirect("/sitio1/pizza")


@login_required
def detalle_pizza(request, pizza_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    return render(request, 'sitio1/DataModelApp/pedidos/detalle_pizza.html', {'datos': pizza})

def registro(request):
    data = {'form' : CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect("/")
        data["form"] = formulario
    
    return render(request, 'registration/registro.html', data)

    #views de la pagina principal 
from django.shortcuts import render

def index(request):
    return render(request, 'sitio1/index.html')