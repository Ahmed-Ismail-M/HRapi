from Attendance.models import Employee
from rest_framework import serializers

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['password', 'username', 'first_name', 'last_name','email']

