from django.shortcuts import render
from rest_framework.views import APIView
from .permissions import IsDoctor
from .models import Patient,PatientData,Medicine
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import (UserSerializer,PatientSerializer,MedicineSerializer,PatientDataSerializer)
# Create your views here.


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class PatientAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            medicine_profile = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(medicine_profile)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"message":"Patient Profile does not exist."},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        try:
            existing_patient = Patient.objects.get(user=request.user)
            return Response({"message": "Patient already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            serializer = PatientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            medicine_profile = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(medicine_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({"message": "Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)   

class MedicineAPIView(APIView):
    permission_classes = [IsDoctor]

    def get(self,request):
        try:
            medicine_profile = Medicine.objects.get(user=request.user)
            serializer = MedicineSerializer(medicine_profile)
            return Response(serializer.data)
        except Medicine.DoesNotExist:
            return Response({"message":"Medicine Profile does not exist."},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        try:
            existing_medicine = Medicine.objects.get(user=request.user)
            return Response({"message": "Medicine already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Medicine.DoesNotExist:
            serializer = MedicineSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            medicine_profile = Medicine.objects.get(user=request.user)
            serializer = MedicineSerializer(medicine_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Medicine.DoesNotExist:
            return Response({"message": "Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)


class PatientDataListCreateAPIView(generics.ListCreateAPIView):
    queryset = PatientData.objects.all()
    serializer_class = PatientDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class PatientDataRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientData.objects.all()
    serializer_class = PatientDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)