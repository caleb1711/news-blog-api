from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy
from unittest.mock import patch


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



# Test Change Password Functionality
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

# Test Forgot Password Feature
        
class ForgotPasswordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_email = "test@example.com"
        self.invalid_email = "invalid_email@example.com"
    @patch('accounts.emails.send_email')
    def test_forgot_password_valid_email(self, mock_send_email):
        response = self.client.post('/api/accounts/user/forget_password/', {"email": self.valid_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_send_email.assert_not_called()
    def test_forgot_password_invalid_email(self):
        response = self.client.post('/api/accounts/user/forget_password/', {"email": self.invalid_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test Reset Password Endpoint

class TestResetPasswordEndpoint(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='test_password')
        self.uid = urlsafe_base64_encode(str(self.user.pk).encode())
        self.token = 'test_token'
        self.reset_password_url = f'/api/accounts/reset/{self.uid}/{self.token}/'

    def test_reset_password_endpoint_success(self):
        new_password = 'new_test_password'
        data = {'password': new_password, 'password1': new_password}
        response = self.client.post(self.reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data['msg'], 'Password Changed Successfully')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_reset_password_endpoint_invalid_token(self):
        invalid_token = 'invalid_token'
        new_password = 'new_test_password'
        data = {'password': new_password, 'password1': new_password}
        invalid_reset_password_url = f'/api/accounts/reset/{self.uid}/{invalid_token}/'
        response = self.client.post(invalid_reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_endpoint_invalid_user(self):
        invalid_user = User.objects.create_user(email='invalid@example.com', password='test_password', id=123456789)
        invalid_uid = urlsafe_base64_encode(str(invalid_user.pk).encode())
        invalid_reset_password_url = f'/api/accounts/reset/{invalid_uid}/{self.token}/'
        new_password = 'new_test_password'
        data = {'password': new_password, 'password1': new_password}
        response = self.client.post(invalid_reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
