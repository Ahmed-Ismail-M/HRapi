from Attendance.models import Attendance, Employee
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['check_in', 'check_out', 'date']
        extra_kwargs = {'date': {'required': True}} 

    def validate(self, attrs):
        # get current check in and out
        check_in = attrs.get('check_in', None) 
        check_out = attrs.get('check_out', None)
        try:
            # get last check in and out
            last_check_in = Attendance.objects.all().filter(
                date=attrs['date']).latest('check_in').check_in
            last_check_out = Attendance.objects.all().filter(
                date=attrs['date']).latest('check_out').check_out
        except Attendance.DoesNotExist:
            last_check_in = None
            last_check_out = None
        if check_in and check_out:
            # check if user logged check in and out
            raise serializers.ValidationError(
                "Only one check per record")
        if not check_in and not check_out:
            # check if user didnt log check in and out
            raise serializers.ValidationError(
                "At least one check per record")
        if check_in:
            # if user logged check in -> 
            if last_check_out:
                if last_check_out >= check_in:
                    raise serializers.ValidationError(
                        f"CHECK IN MUST OCCUR AFTER {last_check_out}")
            if last_check_in:
                if last_check_in >= check_in:
                    raise serializers.ValidationError(
                        f"CHECK IN MUST OCCUR AFTER {check_in}")
        if check_out:
            # if user logged check out -> 
            if not last_check_in:
                raise serializers.ValidationError(
                    "CHECK IN MUST OCCUR BEFORE CHECK OUT")
            if last_check_in:
                if check_out <= last_check_in:
                    raise serializers.ValidationError(
                        f"CHECK OUT MUST OCCUR AFTER {last_check_in}")
            if last_check_out:
                if check_out <= last_check_out:
                    raise serializers.ValidationError(
                        f"CHECK OUT MUST OCCUR AFTER {last_check_out}")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            emp = Employee.objects.get(pk=user.id)
            att = Attendance.objects.create(emp=emp, **validated_data)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Registered employee only")
        return att
