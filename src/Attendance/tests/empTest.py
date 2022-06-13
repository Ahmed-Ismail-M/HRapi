from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client
from Attendance.models import User


class RegisterationTest(APITestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@im-software.net", password="testpass")
        self.client = Client()
        self.client.login(username='admin', password='testpass')
    def tearDown(self):
        self.admin.delete()

    def test_employee(self):
        data = {
            "username": "ahmed", "email": "ahmed@im-software.net", "password": "testpass", }
        response = self.client.post("/api/v1/register", data)
        # assert the registeration completed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
