from Attendance.models import Attendance, Employee
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['check_in', 'check_out', 'date']
        # extra_kwargs = {"check_in": {"required": True}, "check_out": {
        #     "required": True}, "date": {"required": True}}

    def validate(self, data):
        check_in = data.get('check_in', None)
        check_out = data.get('check_out', None)
        if check_in and check_out:
            raise serializers.ValidationError(
                "Only one check per record")
        if not check_in and not check_out:
            raise serializers.ValidationError(
                "At least one check per record")
        attendaces = Attendance.objects.all().filter(date=data['date'])
        if check_in:
            for att in attendaces:
                if att.check_out:
                    if att.check_out >= check_in:
                        raise serializers.ValidationError(
                            "CHECK IN MUST OCCUR AFTER LAST CHECK OUT")
        if check_out:
            if not attendaces:
                raise serializers.ValidationError(
                    "CHECK IN MUST OCCUR BEFORE CHECK OUT")
            for att in attendaces:
                if att.check_in:
                    if check_out <= att.check_in:
                        raise serializers.ValidationError(
                            "CHECK OUT MUST OCCUR AFTER LAST CHECK IN")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            emp = Employee.objects.get(pk=user.id)
            att = Attendance.objects.create(emp=emp, **validated_data)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Registered employee only")
        return att
