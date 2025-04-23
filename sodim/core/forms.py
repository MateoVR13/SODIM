from django import forms
from .models import User, Doctor, EPSMedicationStock


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
