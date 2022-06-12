from Attendance.models import Attendance
from rest_framework import serializers
from datetime import datetime

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
    def validate(self, data):
        today_att = Attendance.objects.all().filter(date=datetime.now(), check='in')
        if not today_att and  data['check'] == 'out':
            raise serializers.ValidationError("you must check in first")
        if data['check'] == 'out' and data['check'] < today_att.date:
            raise serializers.ValidationError("CHECK OUT MUST OCCUR AFTER CHECK IN")
        return data

