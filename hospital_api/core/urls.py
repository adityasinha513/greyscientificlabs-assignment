from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SignupView, CustomTokenObtainPairView, PatientViewSet, MedicalRecordViewSet,
    AddMedicalRecordView, PatientMedicalRecordsView
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'records', MedicalRecordViewSet, basename='record')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/', include('rest_framework.urls')),
    path('patients/<int:patient_id>/add_record/', AddMedicalRecordView.as_view(), name='add_medical_record'),
    path('patients/<int:patient_id>/records/', PatientMedicalRecordsView.as_view(), name='patient_medical_records'),
]

urlpatterns += router.urls 