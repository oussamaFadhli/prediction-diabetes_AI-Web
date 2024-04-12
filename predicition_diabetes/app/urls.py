from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *


urlpatterns = [
    #auth
     path('auth/register/',CreateUserView.as_view(),name="register_user"),
     path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('user/',UserDetailsView.as_view(),name='user_data'),

     path('patient/',PatientAPIView.as_view(),name="patient"),

     path('medicine/',MedicineAPIView.as_view(),name="medicine"),
    

     path('predict-diabetes/', DiabetesPrediction.as_view(), name='predict_diabetes'),
     path('patient-diabetes/',MedicineDiabetesPredicitonDataList.as_view(),name="patient_diabetes_data"),
     path('education-patients/',EducationPatientListAPIView.as_view(),name="education-patient-list"),
     path('create-education-patients/', EducationPatientCreateAPIView.as_view(), name='education-patient-create'),

     path('education-patient/<int:pk>/',EducationPatientRetrieveAPIView.as_view(),name='education-patient-retrieve'),
     path('edit-education-patients/<int:pk>/', EducationPatientUpdateAPIView.as_view(), name='education-patient-update'),
     path('delete-education-patients/<int:pk>/',EducationPatientDestroyAPIView.as_view(),name='education-patient-destroy'),
     path('patient-education-patients/',PatientEducationPatientView.as_view(),name='patient-education-patient-list')

]