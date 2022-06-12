from Attendance.models import Attendance
from rest_framework import serializers

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("check_out must occur after check_in")
        return data

