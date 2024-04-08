from rest_framework import serializers
import re
from .models import Patient , Medicine, PatientData
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

class DiabetesPredictionSerializer(serializers.Serializer):
    pregnancies = serializers.IntegerField()
    glucose = serializers.FloatField()
    blood_pressure = serializers.FloatField()
    skin_thickness = serializers.FloatField()
    insulin = serializers.FloatField()
    bmi = serializers.FloatField()
    diabetes_pedigree_function = serializers.FloatField()
    age = serializers.IntegerField()

    def create(self, validated_data):
        return PatientData.objects.create(**validated_data)