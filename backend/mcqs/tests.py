from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import MCQ

User = get_user_model()

class MCQTests(APITestCase):

    def setUp(self):
        # Create a user and get their JWT token for authenticated requests
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        
        # Create an MCQ
        self.mcq_data = {
            "body": "What is the capital of France?",
            "explanation": "The capital of France is Paris.",
            "options": [
                {"body": "Paris", "is_correct": True},
                {"body": "London", "is_correct": False},
                {"body": "Berlin", "is_correct": False},
                {"body": "Madrid", "is_correct": False}
            ]
        }
        self.create_response = self.client.post(reverse('mcq-list-create'), self.mcq_data, format='json')
        self.mcq_id = self.create_response.data.get('id')

    def test_get_mcqs(self):
        url = reverse('mcq-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_mcq(self):
        url = reverse('mcq-list-create')
        response = self.client.post(url, self.mcq_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['body'], self.mcq_data['body'])
        self.assertIn('id', response.data)

    def test_update_mcq(self):
        if self.mcq_id is None:
            self.fail("MCQ creation failed in setUp.")
        update_data = {
            "body": "What is the capital of Germany?",
            "explanation": "The capital of Germany is Berlin.",
            "options": [
                {"body": "Berlin", "is_correct": True},
                {"body": "Paris", "is_correct": False},
                {"body": "London", "is_correct": False},
                {"body": "Madrid", "is_correct": False}
            ]
        }
        update_url = reverse('mcq-detail', args=[self.mcq_id])
        response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], update_data['body'])

    def test_delete_mcq(self):
        if self.mcq_id is None:
            self.fail("MCQ creation failed in setUp.")
        delete_url = reverse('mcq-detail', args=[self.mcq_id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
