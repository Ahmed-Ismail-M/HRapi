from Attendance.models import Attendance, Employee
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['check_in', 'check_out', 'date']
        extra_kwargs = {'date': {'required': True}} 

    def validate(self, data):
        check_in = data.get('check_in', None)
        check_out = data.get('check_out', None)
        try:
            last_check_in = Attendance.objects.all().filter(
                date=data['date']).latest('check_in').check_in
            last_check_out = Attendance.objects.all().filter(
                date=data['date']).latest('check_out').check_out
        except Attendance.DoesNotExist:
            last_check_in = None
            last_check_out = None
        if check_in and check_out:
            raise serializers.ValidationError(
                "Only one check per record")
        if not check_in and not check_out:
            raise serializers.ValidationError(
                "At least one check per record")
        if check_in:
            if last_check_out:
                if last_check_out >= check_in:
                    raise serializers.ValidationError(
                        "CHECK IN MUST OCCUR AFTER LAST CHECK OUT")
            if last_check_in:
                if last_check_in >= check_in:
                    raise serializers.ValidationError(
                        "CHECK IN MUST OCCUR AFTER LAST CHECK IN")
        if check_out:
            if not last_check_in:
                raise serializers.ValidationError(
                    "CHECK IN MUST OCCUR BEFORE CHECK OUT")
            if last_check_in:
                if check_out <= last_check_in:
                    raise serializers.ValidationError(
                        "CHECK OUT MUST OCCUR AFTER LAST CHECK IN")
            if last_check_out:
                if check_out >= last_check_out:
                    raise serializers.ValidationError(
                        "CHECK OUT MUST OCCUR AFTER LAST CHECK OUT")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            emp = Employee.objects.get(pk=user.id)
            att = Attendance.objects.create(emp=emp, **validated_data)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Registered employee only")
        return att
