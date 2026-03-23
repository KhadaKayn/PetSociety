from django import forms
from .models import TipoMasa, Tamanos, Ingredientes, Productos, Pizza, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Este campo es obligatorio.')
    direccion = forms.CharField(max_length=255, help_text='Dirección de domicilio.')
    telefono = forms.CharField(max_length=15, help_text='Número de teléfono de contacto.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'direccion', 'telefono', 'password1', 'password2']

class UtilidadesForm(forms.ModelForm):
    precio_mes2 = forms.DecimalField(
        label="Nuevo precio del producto",
        max_digits=10, decimal_places=2,
        help_text="Ingrese el nuevo precio del producto"
    )
    promedio_ventas_dia_mes2 = forms.IntegerField(
        label="Nuevo promedio de ventas por día",
        help_text="Ingrese el nuevo promedio de ventas por día"
    )

    class Meta:
        model = Productos
        fields = ['precio', 'costo', 'promedio_ventas_dia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        precio_mes2 = cleaned_data.get('precio_mes2')
        promedio_ventas_dia_mes2 = cleaned_data.get('promedio_ventas_dia_mes2')

        if precio_mes2 is None or promedio_ventas_dia_mes2 is None:
            raise forms.ValidationError("Los campos del nuevo mes son obligatorios.")

        return cleaned_data

    def calcular_utilidades(self):
        cleaned_data = self.cleaned_data
        costo = cleaned_data['costo']
        precio = cleaned_data['precio']
        promedio_ventas_dia = cleaned_data['promedio_ventas_dia']
        precio_mes2 = cleaned_data['precio_mes2']
        promedio_ventas_dia_mes2 = cleaned_data['promedio_ventas_dia_mes2']

        utilidad_mes1 = (precio - costo) * promedio_ventas_dia
        utilidad_mes2 = (precio_mes2 - costo) * promedio_ventas_dia_mes2

        return utilidad_mes1, utilidad_mes2

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'imagen', 'descripcion', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PrecioOptimoForm(forms.ModelForm):
    margen_de_ganancia = forms.DecimalField(max_digits=5, decimal_places=2, help_text="Ingrese el margen de ganancia deseado en %")

    class Meta:
        model = Productos
        fields = ['costo', 'margen_de_ganancia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calcular_precio_optimo(self):
        costo = self.cleaned_data.get('costo')
        margen = self.cleaned_data.get('margen_de_ganancia')
        precio_optimo = costo * (1 + margen / 100)
        return precio_optimo
    
class StockOptimoForm(forms.ModelForm):
    tiempo_entrega_dias = forms.IntegerField(
        label='Tiempo en días para el próximo abastecimiento',
        help_text='El tiempo de entrega es desde que se pide hasta que llega el abastecimiento.'
    )
    stock_seguridad = forms.IntegerField(
        label='Stock de seguridad',
        help_text='El stock de seguridad es una cantidad adicional de inventario que se mantiene para hacer frente a la variabilidad en la demanda y los tiempos de entrega.'
    )

    class Meta:
        model = Productos
        fields = ['promedio_ventas_dia']
        help_texts = {
            'promedio_ventas_dia': 'Base este valor en el promedio de ventas diarias durante un periodo de un mes.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class IngredientesForm(forms.ModelForm):
    class Meta:
        model = Ingredientes
        fields = ['nombre', 'stock', 'precio', 'oferta', 'descuento', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agregar un script de jQuery para mostrar u ocultar el campo de descuento
        self.fields['oferta'].widget.attrs['onclick'] = (
            '$("#id_descuento").toggle(this.checked);'
        )
        self.fields['oferta'].widget.attrs['checked'] = 'checked'

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        oferta = self.cleaned_data.get('oferta')

        if oferta and (descuento < 1 or descuento > 99):
            raise forms.ValidationError("El descuento debe estar entre 1% y 99%.")
        
        return descuento

class TipoMasaForm(forms.ModelForm):
    class Meta:
        model = TipoMasa
        fields = ['nombre', 'disponible', 'precio', 'oferta', 'descuento', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agregar un script de jQuery para mostrar u ocultar el campo de descuento
        self.fields['oferta'].widget.attrs['onclick'] = (
            '$("#id_descuento").toggle(this.checked);'
        )
        self.fields['oferta'].widget.attrs['checked'] = 'checked'


    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        oferta = self.cleaned_data.get('oferta')

        if oferta and (descuento < 1 or descuento > 99):
            raise forms.ValidationError("El descuento debe estar entre 1% y 99%.")
        
        return descuento
    

class TamanosForm(forms.ModelForm):
    class Meta:
        model = Tamanos
        fields = ['nombre', 'disponible', 'precio', 'oferta', 'descuento', 'imagen']
        error_messages = {
            'nombre': {
                'unique': "El tamaño ya existe. Por favor, ingrese un tamaño diferente.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agregar un script de jQuery para mostrar u ocultar el campo de descuento
        self.fields['oferta'].widget.attrs['onclick'] = (
            '$("#id_descuento").toggle(this.checked);'
        )
        self.fields['oferta'].widget.attrs['checked'] = 'checked'

        
    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        oferta = self.cleaned_data.get('oferta')

        if oferta and (descuento < 1 or descuento > 99):
            raise forms.ValidationError("El descuento debe estar entre 1% y 99%.")
        
        return descuento

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['nombre', 'descripcion', 'tamano', 'tipo_masa', 'imagen', 'ingredientes']

    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingredientes.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True  # False Para permitir pizzas sin ingredientes
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Modificar el queryset para incluir solo tamaños disponibles
        self.fields['tamano'].queryset = Tamanos.objects.filter(disponible=True)

        # Modificar el queryset para incluir solo tipos de masa disponibles
        self.fields['tipo_masa'].queryset = TipoMasa.objects.filter(disponible=True)

        # Modificar el queryset para incluir solo ingredientes en stock
        self.fields['ingredientes'].queryset = Ingredientes.objects.filter(stock__gt=0)

    def save(self, commit=True):
        pizza = super().save(commit=False)
        pizza.precio = pizza.calcular_precio()

        if commit:
            pizza.save()

            # Actualizar los ingredientes asociados a la pizza
            pizza.ingredientes.set(self.cleaned_data['ingredientes'])
            pizza.save()

        return pizza

    