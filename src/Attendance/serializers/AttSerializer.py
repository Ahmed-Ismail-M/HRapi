from Attendance.models import Attendance, Employee
from rest_framework import serializers
from datetime import datetime, date


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['check', 'date']
    def validate(self, data):
        # today_att = Attendance.objects.get(date=date.today())
        # if today_att:
        #     if today_att.check == data['check']:
        #         print(date.today(), today_att.check)
        #     raise serializers.ValidationError("you must check in first")
        # if data['check'] == 'out' and data['check'] < today_att.date:
        #     raise serializers.ValidationError("CHECK OUT MUST OCCUR AFTER CHECK IN")
        return data
    def create(self, validated_data):
        user = self.context['request'].user
        try:
            emp = Employee.objects.get(pk = user.id)
            att = Attendance.objects.create(emp=emp, **validated_data)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Registered employee only")
        return att