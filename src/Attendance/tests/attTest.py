from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client
from Attendance.models import Employee


class AddAtt(APITestCase):
    def setUp(self) -> None:
        self.emp = Employee.objects.create(
            username="admin", email="admin@im-software.net", password="testpass")
        self.client = Client()
        self.client.login(username='admin', password='testpass')
    def tearDown(self):
        self.emp.delete()

    def test_att(self):
        data = {
            "emp":self.emp.id, "check": "in", "date": "2022-1-1T6:30", }
        response = self.client.post("/api/v1/attendance", data)
        print(response.content)
        # assert the registeration completed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
