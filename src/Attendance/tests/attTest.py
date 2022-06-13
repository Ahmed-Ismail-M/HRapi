from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client
from Attendance.models import Attendance


class AddAtt(APITestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@im-software.net", password="testpass")
        self.client = Client()
        self.client.login(username='admin', password='testpass')

    def test_att(self):
        data = {
            "emp": "1", "check": "in", "date": "2022-1-1 6:30AM", }
        response = self.client.post("/api/v1/att", data)
        # assert the registeration completed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
