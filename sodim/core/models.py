import random
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Base class for timestamps
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# EPS (Healthcare provider)
class EPS(TimestampedModel):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    is_distributor = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Doctor
class Doctor(TimestampedModel):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    specialty = models.CharField(max_length=100, blank=True)
    eps = models.ForeignKey(EPS, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Patient
class Patient(TimestampedModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    PRIORITY_GROUPS = [
        ('CHILD', 'Child'),
        ('SENIOR', 'Senior'),
        ('CHRONIC', 'Chronic Disease'),
        ('CONTROL', 'Controlled Medication'),
        ('REGULAR', 'Regular'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    identification_number = models.CharField(max_length=50, unique=True)

    eps = models.ForeignKey(EPS, on_delete=models.CASCADE, related_name='patients')

    # Socioeconomic Information
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    socioeconomic_stratum = models.PositiveSmallIntegerField()
    income = models.DecimalField(max_digits=10, decimal_places=2)

    priority_group = models.CharField(max_length=10, choices=PRIORITY_GROUPS)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Medication
class Medication(TimestampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# EPS Medication Stock
class EPSMedicationStock(TimestampedModel):
    eps = models.ForeignKey(EPS, on_delete=models.CASCADE, related_name='medication_stocks')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('eps', 'medication')
        
    def __str__(self):
        return f"{self.eps.name} - {self.medication.name} ({self.quantity})"

# Prescription
class Prescription(TimestampedModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.patient} - {self.medication}"

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='DOCTOR', **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'EPS_ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    ROLE_CHOICES = [
        ('EPS_ADMIN', 'EPS Administrator'),
        ('DOCTOR', 'Doctor'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    eps = models.ForeignKey('EPS', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('sent', 'Sent'),
        ('arrived', 'Arrived'),
        ('delivered', 'Delivered'),
    ]

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='orders')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='orders')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
    estimated_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Order for {self.medication.name} - {self.status}"

    def generate_estimated_delivery(self):
        # Si no hay stock, el medicamento tardará entre 1 y 3 días
        if self.status == 'requested':
            days = random.randint(1, 3)
            self.estimated_delivery_date = self.prescription.created_at.date() + timedelta(days=days)
            self.save()

    def mark_as_sent(self):
        self.status = 'sent'
        self.save()

    def mark_as_arrived(self):
        self.status = 'arrived'
        self.save()

    def mark_as_delivered(self):
        self.status = 'delivered'
        self.actual_delivery_date = self.prescription.created_at.date()
        self.save()

