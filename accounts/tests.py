from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
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




class ChangePasswordAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test_user@example.com', password='test_password')
        self.client.force_authenticate(user=self.user)

    def test_change_password(self):
        url = '/api/accounts/user/change_password/'
        data = {
            'old_password': 'test_password',
            'password': 'new_password',
            'password1': 'new_password'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_change_password_unauthenticated(self):
        self.client.logout()
        
        url = '/api/accounts/user/change_password/'
        data = {
            'old_password': 'test_password',
            'password': 'new_password',
            'password1': 'new_password'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
