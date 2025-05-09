from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Patient, Doctor, User, EPSMedicationStock, Prescription, Order
from .forms import EPSMedicationStockForm, PrescriptionForm, CustomLoginForm


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión - SODIM System'
        return context

def LandingPage(request):
    return render(request, 'core/landing.html')

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
    
    @login_required
    def eps_dashboard(request):
        """
        View for the EPS admin dashboard showing key statistics and data
        """
        # Check if user is associated with an EPS and is an EPS_ADMIN
        if not request.user.eps or request.user.role != 'EPS_ADMIN':
            return render(request, 'core/access_denied.html')
        
        # Get user's EPS
        eps = request.user.eps
        
        # Basic statistics
        patients_count = Patient.objects.filter(eps=eps).count()
        doctors_count = Doctor.objects.filter(eps=eps).count()
        prescriptions_count = Prescription.objects.filter(doctor__eps=eps).count()
        pending_orders_count = Order.objects.filter(
            patient__eps=eps, 
            status__in=['requested', 'sent', 'arrived']
        ).count()
        
        # Recent orders (last 10)
        recent_orders = Order.objects.filter(
            patient__eps=eps
        ).select_related('patient', 'medication').order_by('-created_at')[:10]
        
        # Medication stock for this EPS
        medication_stocks = EPSMedicationStock.objects.filter(
            eps=eps
        ).select_related('medication').order_by('quantity')
        
        # Priority patients (non-regular)
        priority_patients = Patient.objects.filter(
            eps=eps, 
            priority_group__in=['CHILD', 'SENIOR', 'CHRONIC', 'CONTROL']
        ).order_by('priority_group')[:10]
        
        # Recent prescriptions
        recent_prescriptions = Prescription.objects.filter(
            doctor__eps=eps
        ).select_related('patient', 'doctor', 'medication').order_by('-created_at')[:10]
        
        context = {
            'patients_count': patients_count,
            'doctors_count': doctors_count,
            'prescriptions_count': prescriptions_count,
            'pending_orders_count': pending_orders_count,
            'recent_orders': recent_orders,
            'medication_stocks': medication_stocks,
            'priority_patients': priority_patients,
            'recent_prescriptions': recent_prescriptions,
        }
        
        return render(request, 'core/eps_dashboard.html', context)

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

# Ver prescripciones de médicos para su EPS
class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'core/prescription_list.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        # Filtramos solo por médicos y pacientes de la misma EPS
        return Prescription.objects.filter(doctor__eps=self.request.user.eps)

class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'core/prescription_form.html'
    success_url = reverse_lazy('prescription_list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor  # Asignar el médico autenticado
        response = super().form_valid(form)

        # Crear una orden de entrega automáticamente para la prescripción
        order = Order.objects.create(
            prescription=form.instance,
            patient=form.instance.patient,
            medication=form.instance.medication,
        )

        # Generar la fecha de entrega estimada
        order.generate_estimated_delivery()
        return response

def OrderStatus(request):
    if request.method == 'GET':
        patient_id = request.GET.get('patient_id')
        order_number = request.GET.get('order_number')

        try:
            order = Order.objects.get(patient__identification_number=patient_id, id=order_number)
            return render(request, 'core/order_status.html', {'order': order})
        except Order.DoesNotExist:
            return render(request, 'core/order_status.html', {'error': 'Order not found.'})
