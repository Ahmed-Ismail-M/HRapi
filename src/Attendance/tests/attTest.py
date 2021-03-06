from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client
from Attendance.models import Employee
from django.contrib.auth.models import Group


class AddAtt(APITestCase):
    def setUp(self) -> None:
        self.emp = Employee.objects.create(
            username="admin", email="admin@im-software.net", is_superuser=True
        )
        self.emp.set_password("testpass")
        group, created = Group.objects.get_or_create(name="Employee")
        group.save()
        self.emp.groups.add(group)
        self.emp.save()
        self.client = Client()
        self.client.login(username="admin", password="testpass")

    def tearDown(self):
        self.emp.delete()

    def test_att(self):
        data = {"check_in": "1:30", "date": "2022-1-1"}
        response = self.client.post("/api/v1/attendance", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_check_out(self):
        data = {"check_in": "1:30", "date": "2022-1-1"}
        self.client.post("/api/v1/attendance", data)
        data = {"date": "2022-1-1", "check_out": "1:40"}
        response = self.client.post("/api/v1/attendance", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_check_out(self):
        data = {"date": "2022-1-1", "check_out": "1:00"}
        response = self.client.post("/api/v1/attendance", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content, b'{"non_field_errors":["PLEASE CHECK IN FIRST"]}'
        )

    def test_get_att(self):
        self.test_valid_check_out()
        self.client.login(username="admin", password="testpass")
        response = self.client.get("/api/v1/allattendances")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
