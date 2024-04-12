from django.contrib import admin
from .models import User,Patient,Medicine,PatientData,EducationPatient
# Register your models here.


admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(PatientData)
admin.site.register(EducationPatient)