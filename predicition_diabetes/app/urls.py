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
    path('patient-data/', PatientDataListCreateAPIView.as_view(), name='patient-data-list-create'),
    path('patient-data/<int:pk>/', PatientDataRetrieveUpdateDestroyAPIView.as_view(), name='patient-data-retrieve-update-destroy'),

    path('medicine/',MedicineAPIView.as_view(),name="medicine"),

]