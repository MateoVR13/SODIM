from django import forms
from .models import User, Doctor, EPSMedicationStock, Prescription
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']
    
    username = forms.EmailField(label='Email')  # Override username field with email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos las clases de Bootstrap a los campos
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
            'required': 'required',
            'autocomplete': 'email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••',
            'required': 'required',
            'autocomplete': 'current-password'
        })
        # Mensajes de error personalizados
        self.error_messages = {
            'invalid_login': "Por favor, introduzca un correo electrónico y contraseña correctos.",
            'inactive': "Esta cuenta está inactiva. Por favor, contacte al administrador.",
        }

class DoctorUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def save(self, commit=True, eps=None):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'DOCTOR'
        if eps:
            user.eps = eps
        if commit:
            user.save()
        return user

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['license_number', 'specialty']

class EPSMedicationStockForm(forms.ModelForm):
    class Meta:
        model = EPSMedicationStock
        fields = ['medication', 'quantity']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'dosage', 'frequency', 'duration_days', 'notes']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de estilo a los campos
        self.fields['patient'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione un paciente'
        })
        self.fields['medication'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seleccione un medicamento'
        })
        self.fields['dosage'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: 1 tableta, 5ml, etc.'
        })
        self.fields['frequency'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: Cada 8 horas, una vez al día'
        })
        self.fields['duration_days'].widget.attrs.update({
            'class': 'form-control',
            'min': '1',
            'type': 'number'
        })
        self.fields['notes'].widget.attrs.update({
            'class': 'form-control form-control-textarea',
            'placeholder': 'Instrucciones especiales, precauciones, etc.',
            'rows': '4'
        })