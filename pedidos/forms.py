from django import forms
from .models import Pedido
from catalogo.models import Producto


class PedidoForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    
    # Campo honeypot (anti-spam)
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label=''
    )

    class Meta:
        model = Pedido
        fields = ['nombre', 'whatsapp', 'producto', 'cantidad', 'texto_tallar', 'fecha_para_cuando', 'entrega', 'zona_ciudad', 'notas', 'website']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu nombre',
                'required': True
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+54 9 11 1234-5678 o 5491112345678',
                'type': 'tel',
                'required': True
            }),
            'texto_tallar': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Ej: "María y Juan - 15/03/2024" o "Feliz cumpleaños"',
                'rows': 3
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'value': 1,
                'required': True
            }),
            'fecha_para_cuando': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'entrega': forms.RadioSelect(attrs={
                'class': 'form-radio'
            }),
            'zona_ciudad': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: CABA, Zona Norte, etc.'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Algo más a tener en cuenta...',
                'rows': 2
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer zona_ciudad no requerido por defecto
        self.fields['zona_ciudad'].required = False

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if not whatsapp:
            raise forms.ValidationError("Por favor ingresa un número de WhatsApp.")
        
        # Normalizar: aceptar +54, espacios, guiones
        # Remover espacios, guiones, paréntesis y el símbolo +
        whatsapp_limpio = whatsapp.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        
        # Si empieza con 54 (Argentina), mantenerlo
        # Si empieza con 9 y tiene 10 dígitos, agregar 54
        # Si solo tiene dígitos, verificar longitud
        if whatsapp_limpio.startswith('54'):
            whatsapp_normalizado = whatsapp_limpio
        elif whatsapp_limpio.startswith('9') and len(whatsapp_limpio) == 10:
            # Formato local argentino: agregar código de país
            whatsapp_normalizado = '54' + whatsapp_limpio
        elif whatsapp_limpio.startswith('0'):
            # Si empieza con 0, removerlo y agregar 54
            whatsapp_normalizado = '54' + whatsapp_limpio[1:]
        else:
            whatsapp_normalizado = whatsapp_limpio
        
        # Validar que solo tenga dígitos y longitud mínima
        if not whatsapp_normalizado.isdigit():
            raise forms.ValidationError(
                "Por favor ingresa un número de WhatsApp válido. "
                "Ejemplos: +54 9 11 1234-5678, 5491112345678, 91112345678"
            )
        
        if len(whatsapp_normalizado) < 10:
            raise forms.ValidationError(
                "El número de WhatsApp debe tener al menos 10 dígitos. "
                "Ejemplo: +54 9 11 1234-5678 o 5491112345678"
            )
        
        return whatsapp_normalizado

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 1:
            raise forms.ValidationError("La cantidad debe ser al menos 1.")
        return cantidad
    
    def clean_website(self):
        """Honeypot: si se completa, es spam"""
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError("")
        return website
    
    def clean(self):
        cleaned_data = super().clean()
        entrega = cleaned_data.get('entrega')
        zona_ciudad = cleaned_data.get('zona_ciudad')
        
        # Si eligió envío, zona_ciudad es requerido
        if entrega == 'envio' and not zona_ciudad:
            raise forms.ValidationError({
                'zona_ciudad': 'Por favor indica la zona o ciudad para el envío.'
            })
        
        return cleaned_data
