from django.shortcuts import render
from rest_framework.views import APIView
from .permissions import IsDoctor
from rest_framework.response import Response
from .models import Patient,PatientData,Medicine
import numpy as np
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import generics,status

from .serializers import (UserSerializer,PatientSerializer,MedicineSerializer,DiabetesPredictionSerializer)
from app.diabetes_ai.diabetes_ai import predict_diabetes
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


class DiabetesPrediction(APIView):
    def post(self, request):
        serializer = DiabetesPredictionSerializer(data=request.data)
        if serializer.is_valid():
            # Save user input to PatientData model
            patient_data = serializer.save()
            # Make prediction using AI model
            prediction_percentage = predict_diabetes(serializer.validated_data)
            # Update prediction_percentage in PatientData model
            patient_data.prediction_percentage = prediction_percentage
            patient_data.save()
            return Response({"prediction_percentage": round(prediction_percentage, 2)}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)