from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(User):
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    # Puedes agregar más campos personalizados según sea necesario

    def __str__(self):
        return self.username

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="productos", null=True, blank=True)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    margen_de_ganancia = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    stock = models.PositiveIntegerField(null=True)
    stock_optimo = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    promedio_ventas_dia = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    utilidades_anteriores = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    utilidades_actuales = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class Ingredientes(models.Model):                                                                                       #REALIZADO/COMPLETADO=100%
    nombre = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    oferta = models.BooleanField(default=False)
    descuento = models.DecimalField(max_digits=2, decimal_places=0, default=0, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to="ingredientes", null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Imprimir valores antes de la validación
        print(f"Oferta: {self.oferta}, Descuento: {self.descuento}")

        if self.oferta:
            self.precio -= (self.precio * self.descuento) / 100

        # Llamar al método save de la clase base
        super().save(*args, **kwargs)

class TipoMasa(models.Model):                                                                                           #REALIZADO
    nombre = models.CharField(max_length=50, unique=True)
    disponible = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    oferta = models.BooleanField(default=False)
    descuento = models.DecimalField(max_digits=2, decimal_places=0, default=0, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to="masas", null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Imprimir valores antes de la validación
        print(f"Oferta: {self.oferta}, Descuento: {self.descuento}")

        if self.oferta:
            self.precio -= (self.precio * self.descuento) / 100

        # Llamar al método save de la clase base
        super().save(*args, **kwargs)
    
    
    
class Tamanos(models.Model):                                                                                            #REALIZADO
    nombre = models.CharField(max_length=50, unique=True)
    disponible = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    oferta = models.BooleanField(default=False)
    descuento = models.DecimalField(max_digits=2, decimal_places=0, default=0, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to="tamanos", null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Imprimir valores antes de la validación
        print(f"Oferta: {self.oferta}, Descuento: {self.descuento}")

        if self.oferta:
            self.precio -= (self.precio * self.descuento) / 100

        # Llamar al método save de la clase base
        super().save(*args, **kwargs)   

class Pizza(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tamano = models.ForeignKey(Tamanos, on_delete=models.CASCADE)
    tipo_masa = models.ForeignKey(TipoMasa, on_delete=models.CASCADE)
    ingredientes = models.ManyToManyField(Ingredientes, through='PizzaIngredientes')
    precio = models.DecimalField(max_digits=10, decimal_places=0, null=True) #realizar logica de precio
    imagen = models.ImageField(upload_to="imagen", null=True, blank=True)

    def calcular_precio(self):
        precio_tamano = self.tamano.precio
        precio_masa = self.tipo_masa.precio

        # Guardar la instancia de Pizza para obtener un ID
        super().save()

        # Recargar la instancia para obtener los ingredientes
        pizza_con_id = Pizza.objects.get(id=self.id)
        
        # Calcular el precio de los ingredientes
        precio_ingredientes = sum(ingrediente.precio for ingrediente in pizza_con_id.ingredientes.all())

        # Calcular el precio total
        precio_total = precio_tamano + precio_masa + precio_ingredientes

        return precio_total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Calcular el precio después de guardar la instancia
        self.precio = self.calcular_precio()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class PizzaIngredientes(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingredientes, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('pizza', 'ingrediente',)
    
    def __str__(self):
        return f"{self.pizza.nombre} - {self.ingrediente.nombre}"

    
class PedidoCliente(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, default='Pendiente')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    direccion_entrega = models.CharField(max_length=255) 
    telefono_contacto = models.CharField(max_length=15)

class DetalleCompra(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=8, decimal_places=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Detalle de compra - {self.pizza} - {self.fecha_compra} - {self.precio_total}"

class Permiso(models.Model):
    pass
#modelo de la pagina principal 

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name