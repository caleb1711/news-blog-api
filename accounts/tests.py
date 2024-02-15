from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

# Test User Creation Endpoint
class UserCreationEndpointTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_user_data = {
            "email": "test@example.com",
            "password": "test_password"
        }
        self.invalid_user_data = {
            "email": "invalid_email",
            "password": "short"
        }

    def test_create_user_valid_data(self):
        response = self.client.post('/api/accounts/user/', self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.valid_user_data['email']).exists())

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/accounts/user/', self.invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email=self.invalid_user_data['email']).exists())

    def test_create_user_authenticated(self):
        user = User.objects.create_user(email='auth_user@example.com', password='test_password')
        self.client.force_login(user)

        response = self.client.post('/api/accounts/user/', self.valid_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
