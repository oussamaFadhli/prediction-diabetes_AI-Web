from rest_framework import serializers
import re
from .models import Patient , Medicine, PatientData , EducationPatient
from django.contrib.auth import get_user_model




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate_password(self, value):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).*$', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter and one digit."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = self.validate_password(password)
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = self.validate_password(password)
        return super().update(instance, validated_data)


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class MedicineSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Medicine
        fields = '__all__'

class DiabetesPredictionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PatientData
        fields = '__all__'

class EducationPatientCreateSerializer(serializers.ModelSerializer):  
    class Meta:
        model = EducationPatient
        fields = '__all__'

class EducationPatientListSerializer(serializers.ModelSerializer):
    patient_data = DiabetesPredictionSerializer(read_only=True)
    class Meta:
        model = EducationPatient
        fields = '__all__'

class EducationPatientSerializer(serializers.ModelSerializer):  
    class Meta:
        model = EducationPatient
        fields = '__all__'