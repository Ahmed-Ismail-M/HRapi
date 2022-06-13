from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client
from django.contrib.auth import get_user_model

class RegisterationTest(APITestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin", email="admin@im-software.net", password="testpass")
        self.client = Client()
        self.client.login(username='admin', password='testpass')
    def tearDown(self):
        self.admin.delete()

    def test_register(self):
        data = {
            "username": "ahmed", "email": "ahmed@im-software.net", "password": "testpass", }
        response = self.client.post("/api/v1/register", data)
        # assert the registeration completed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_login(self):
        data = {
            "username": self.admin.username, "password": "testpass",}
        response = self.client.post("/api/v1/login", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
