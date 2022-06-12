from Attendance.models import Attendance
from rest_framework import serializers
from datetime import date

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
    def validate(self, data):
        today_att = Attendance.objects.all().filter(date=date.today)
        if today_att:
            if data['check'] == 'out' and today_att.check != 'in':
                raise serializers.ValidationError("you must check in first")
        return data

