from Attendance.models import Attendance, Employee
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['check_in', 'check_out', 'date']
        extra_kwargs = {"check_in": {"required": True}, "check_out": {
            "required": True}, "date": {"required": True}}

    def validate(self, data):
        attendaces = Attendance.objects.all().filter(date=data['date'])
        for att in attendaces:
            if att.check_out >= data['check_in']:
                raise serializers.ValidationError(
                    "CHECK IN MUST OCCUR AFTER LAST CHECK OUT")
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError(
                "CHECK OUT MUST OCCUR AFTER CHECK IN")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            emp = Employee.objects.get(pk=user.id)
            att = Attendance.objects.create(emp=emp, **validated_data)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Registered employee only")
        return att
