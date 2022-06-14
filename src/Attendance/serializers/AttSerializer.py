from Attendance.models import Attendance, Employee
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["check_in", "check_out", "date"]
        extra_kwargs = {"date": {"required": True}}

    def validate(self, attrs):
        # get current check in and out
        user = self.context["request"].user
        check_in = attrs.get("check_in", None)
        check_out = attrs.get("check_out", None)
        date = attrs.get("date", None)
        try:
            # get last check in and out
            last_record = (
                Attendance.objects.all().filter(date=attrs["date"], emp=user).last()
            )
            # get last check in and out
            last_check_in = (
                Attendance.objects.all()
                .filter(date=date, emp=user)
                .latest("check_in")
                .check_in
            )
            last_check_out = (
                Attendance.objects.all()
                .filter(date=date, emp=user)
                .latest("check_out")
                .check_out
            )
        except Attendance.DoesNotExist:
            last_record = None
            last_check_in = None
            last_check_out = None
        if check_in and check_out:
            # check if user logged check in and out
            raise serializers.ValidationError("Only one check per record")
        if not check_in and not check_out:
            # check if user didnt log check in and out
            raise serializers.ValidationError("At least one check per record")
        if last_record:
            if check_in:
                # if user logged check in ->
                if last_record.is_attending:
                    raise serializers.ValidationError("PLEASE CHECK OUT FIRST")
                else:
                    if last_check_in:
                        if last_check_in >= check_in:
                            raise serializers.ValidationError(
                                f"CHECK IN MUST OCCUR AFTER {last_check_in}"
                            )
            if check_out:
                # if user logged check out ->
                if not last_record.is_attending:
                    raise serializers.ValidationError("PLEASE CHECK IN FIRST")
                else:
                    if last_check_out:
                        if last_check_out >= check_out:
                            raise serializers.ValidationError(
                                f"CHECK OUT MUST OCCUR AFTER {last_check_out}"
                            )
                    if last_check_in:
                        if last_check_in >= check_out:
                            raise serializers.ValidationError(
                                f"CHECK OUT MUST OCCUR AFTER {last_check_in}"
                            )
        else:
            if check_out:
                raise serializers.ValidationError("PLEASE CHECK IN FIRST")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        check_in = validated_data.get("check_in", None)
        try:
            validated_data["is_attending"] = True if check_in else False
            emp = Employee.objects.get(pk=user.id)
            att = Attendance.objects.create(emp=emp, **validated_data)
        except Employee.DoesNotExist as emp_not_exited:
            raise serializers.ValidationError(
                "Registered employee only"
            ) from emp_not_exited
        return att
class AttendancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'