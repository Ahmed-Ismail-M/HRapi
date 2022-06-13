from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client
from Attendance.models import Employee
from django.contrib.auth.models import Group


class AddAtt(APITestCase):
    def setUp(self) -> None:
        self.emp = Employee.objects.create(
            username="admin", email="admin@im-software.net")
        self.emp.set_password('testpass')
        group, created = Group.objects.get_or_create(name='Employee')
        group.save()
        self.emp.groups.add(group)
        self.emp.save()
        self.client = Client()
        self.client.login(username='admin', password='testpass')

    def tearDown(self):
        self.emp.delete()

    def test_att(self):
        data = {"check_in": "1:30", "date": "2022-1-1", }
        response = self.client.post("/api/v1/attendance", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
