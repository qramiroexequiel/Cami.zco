from django import forms
from .models import Consulta


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nombre', 'whatsapp', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu nombre',
                'required': True
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '5491112345678',
                'type': 'tel',
                'required': True
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Escribe tu consulta...',
                'rows': 5,
                'required': True
            }),
        }

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        # Limpiar espacios y caracteres especiales
        whatsapp = ''.join(filter(str.isdigit, whatsapp))
        if len(whatsapp) < 10:
            raise forms.ValidationError("Por favor ingresa un número de WhatsApp válido.")
        return whatsapp

