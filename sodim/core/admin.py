from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EPS, Doctor, Patient, Medication, EPSMedicationStock, Prescription, Order

# Formulario personalizado para crear usuarios
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'role', 'eps')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Formulario personalizado para editar usuarios
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'role', 'eps', 'is_active', 'is_staff', 'is_superuser')

# Admin personalizado para User
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('email', 'role', 'eps', 'is_staff')
    list_filter = ('role', 'eps')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'role', 'eps')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'eps', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(EPS)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Medication)
admin.site.register(EPSMedicationStock)
admin.site.register(Prescription)
admin.site.register(Order)
