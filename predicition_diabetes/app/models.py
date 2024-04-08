from django.db import models
from .managers import CustomUserManager
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Patient(models.Model):
    first_name = models.CharField(max_length=255,null=False)
    last_name = models.CharField(max_length=255,null=False)
    birthday = models.DateField()
    address = models.CharField(max_length=255)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="patient_user")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Medicine(models.Model):
    first_name = models.CharField(max_length=255,null=False)
    last_name = models.CharField(max_length=255,null=False)
    birthday = models.DateField()
    DOCTOR_SPECIALITIES = {
    "IM": "Internal medicine",
    "FM": "Family medicine",
    "SG": "Surgery",
    "EM": "Emergency medicine",
    "GM": "Gastroenterology",
    "CM": "Cardiology",
    "PM": "Psychiatry",
    }
    speciality = models.CharField(max_length=50,choices=DOCTOR_SPECIALITIES)
    address = models.CharField(max_length=255)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="medicine_user")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class PatientData(models.Model):
    pregnancies = models.IntegerField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree_function = models.FloatField()
    age = models.IntegerField()
    prediction_percentage = models.FloatField(null=True, blank=True)