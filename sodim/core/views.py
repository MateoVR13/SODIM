from django import forms
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Doctor, User, EPSMedicationStock
from .forms import EPSMedicationStockForm

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.role == 'EPS_ADMIN':
            return reverse_lazy('eps_dashboard')
        else:
            return reverse_lazy('doctor_dashboard')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# Dashboards
class EPSDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/eps_dashboard.html'

class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/doctor_dashboard.html'

# Restricción para EPS Admin
class EPSAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'EPS_ADMIN'

# Listar médicos
class DoctorListView(EPSAdminRequiredMixin, ListView):
    model = Doctor
    template_name = 'core/doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        # Solo los médicos de la EPS del admin
        return Doctor.objects.filter(eps=self.request.user.eps)

# Formulario para crear doctor
class DoctorForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'license_number', 'specialty']

class DoctorCreateView(EPSAdminRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

    def form_valid(self, form):
        email = form.cleaned_data.pop('email')
        password = form.cleaned_data.pop('password')

        # Crear el usuario
        user = User.objects.create_user(
            email=email,
            password=password,
            role='DOCTOR',
            eps=self.request.user.eps
        )

        form.instance.user = user
        form.instance.eps = self.request.user.eps
        return super().form_valid(form)
    
class DoctorUpdateView(EPSAdminRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

    def get_queryset(self):
        # Solo permitir editar médicos de la misma EPS
        return Doctor.objects.filter(eps=self.request.user.eps)

class DoctorDeleteView(EPSAdminRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'core/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

    def get_queryset(self):
        return Doctor.objects.filter(eps=self.request.user.eps)


# Ver inventario de medicamentos
class EPSMedicationStockListView(EPSAdminRequiredMixin, ListView):
    model = EPSMedicationStock
    template_name = 'core/medication_stock_list.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        return EPSMedicationStock.objects.filter(eps=self.request.user.eps)

# Agregar nuevo medicamento al stock
class EPSMedicationStockCreateView(EPSAdminRequiredMixin, CreateView):
    model = EPSMedicationStock
    form_class = EPSMedicationStockForm
    template_name = 'core/medication_stock_form.html'
    success_url = reverse_lazy('medication_stock_list')

    def form_valid(self, form):
        form.instance.eps = self.request.user.eps
        return super().form_valid(form)