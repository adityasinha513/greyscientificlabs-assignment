from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Patient, MedicalRecord
from .serializers import (
    SignupSerializer, PatientSerializer, MedicalRecordSerializer, CustomTokenObtainPairSerializer
)
from .permissions import IsDoctorAndOwner
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorAndOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Patient.objects.all()
        return Patient.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'], url_path='records')
    def records(self, request, pk=None):
        patient = self.get_object()
        if not (request.user.is_superuser or patient.created_by == request.user):
            return Response({'detail': 'Not found.'}, status=404)
        records = patient.medical_records.all()
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return MedicalRecord.objects.all()
        if user.role == 'doctor':
            return MedicalRecord.objects.filter(patient__created_by=user)
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        patient = serializer.validated_data['patient']
        if not (self.request.user.is_superuser or patient.created_by == self.request.user):
            raise serializers.ValidationError("You can only add records to your own patients.")
        serializer.save()

class AddMedicalRecordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
            if not (request.user.is_superuser or patient.created_by == request.user):
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientMedicalRecordsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
            if not (request.user.is_superuser or patient.created_by == request.user):
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        records = patient.medical_records.all()
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
