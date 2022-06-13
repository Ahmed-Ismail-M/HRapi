from Attendance.models import Attendance, Employee
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['check_in', 'check_out', 'date']
        # extra_kwargs = {"check_in": {"required": True}, "check_out": {
        #     "required": True}, "date": {"required": True}}

    def validate(self, data):
        check_in = data.pop('check_in', None)
        check_out = data.pop('check_out', None)
        if check_in and check_out:
            raise serializers.ValidationError(
                        "Only one check per record")
        attendaces = Attendance.objects.all().filter(date=data['date'])
        if check_in:
            for att in attendaces:
                if att.check_out >= data['check_in']:
                    raise serializers.ValidationError(
                        "CHECK IN MUST OCCUR AFTER LAST CHECK OUT")
        if check_out:
            for att in attendaces:
                if check_out <= att.check_out:
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
