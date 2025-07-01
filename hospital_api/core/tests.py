from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()

class AuthTests(APITestCase):
    def test_signup_and_login(self):
        signup_url = reverse('signup')
        data = {'username': 'doc1', 'password': 'pass123', 'role': 'doctor'}
        resp = self.client.post(signup_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='doc1').exists())

        login_url = reverse('token_obtain_pair')
        resp = self.client.post(login_url, {'username': 'doc1', 'password': 'pass123'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.token = resp.data['access']

class PatientAccessTests(APITestCase):
    def setUp(self):
        self.doc1 = User.objects.create_user(username='doc1', password='pass123', role='doctor')
        self.doc2 = User.objects.create_user(username='doc2', password='pass123', role='doctor')
        self.p1 = Patient.objects.create(name='Alice', age=30, gender='female', address='Addr1', created_by=self.doc1)
        self.p2 = Patient.objects.create(name='Bob', age=40, gender='male', address='Addr2', created_by=self.doc2)
        login_url = reverse('token_obtain_pair')
        resp = self.client.post(login_url, {'username': 'doc1', 'password': 'pass123'})
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_doctor_sees_only_own_patients(self):
        url = reverse('patient-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], 'Alice')

    def test_doctor_cannot_access_others_patient_detail(self):
        url = reverse('patient-detail', args=[self.p2.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_doctor_can_access_own_patient_detail(self):
        url = reverse('patient-detail', args=[self.p1.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Alice')
