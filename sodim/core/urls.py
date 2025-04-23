from django.urls import path
from .views import CustomLoginView, CustomLogoutView, EPSDashboardView, DoctorDashboardView, DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView, EPSMedicationStockListView, EPSMedicationStockCreateView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('eps/dashboard/', EPSDashboardView.as_view(), name='eps_dashboard'),
    path('doctor/dashboard/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('eps/doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('eps/doctors/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('eps/doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name='doctor_edit'),
    path('eps/doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor_delete'),
    path('eps/medications/', EPSMedicationStockListView.as_view(), name='medication_stock_list'),
    path('eps/medications/add/', EPSMedicationStockCreateView.as_view(), name='medication_stock_add'),
]