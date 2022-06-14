from rest_framework import generics
from datetime import datetime
from Attendance.models import Attendance
from Attendance.serializers.AttSerializer import AttendanceSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from Attendance.middleware import auth_required, allowed_users
from rest_framework.decorators import api_view


def calc_working_hrs(check_in: datetime, check_out: datetime):
    return str(check_in - check_out)


class Create(generics.GenericAPIView):

    serializer_class = AttendanceSerializer

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Employee"]))
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Index(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.all().filter(emp=self.request.user.id)
        return queryset


@api_view()
def DailyIndex(request):
    daily_atts = Attendance.objects.all().filter(emp=request.user.id)
    result = {}
    for index, att in enumerate(daily_atts):
        stri = str(index)
        str_date = att.date.strftime("%d/%m/%Y")
        if str_date not in result:
            if att.check_in:
                result[str_date] = {
                    f"In-{stri}": att.check_in,
                    "Status": "Late" if Attendance.check_late(att.check_in) else "",
                }
            if att.check_out:
                result[str_date] = {f"Out-{stri}": att.check_out}
        else:
            if att.check_in:
                result[str_date][f"In-{stri}"] = att.check_in
            if att.check_out:
                result[str_date][f"Out-{stri}"] = att.check_out
                result[str_date][f"Status"] = (
                    "Early Leave" if Attendance.check_early_leave(att.check_out) else ""
                )
    return Response(result)


@api_view()
def DailyReport(request):
    daily_atts = (
        Attendance.objects.all()
        .filter(emp=request.user.id)
        .values_list("date", flat=True)
        .distinct()
    )
    result = {}
    for date in daily_atts:
        str_date = date.strftime("%d/%m/%Y")
        # get last check in and out
        first_check_in = (
            Attendance.objects.all()
            .filter(date=date)
            .order_by("check_in")
            .exclude(check_in__isnull=True)[0]
            .check_in
        )
        last_check_out = (
            Attendance.objects.all().filter(date=date).latest("check_out").check_out
        )
        result[str_date] = {
            "Arrival": "Late"
            if Attendance.check_late(first_check_in)
            else "Within Time",
            "Leaving": "Early"
            if Attendance.check_early_leave(last_check_out)
            else "Within Time",
            "Working Time": Attendance.calculate_wroking_time(
                check_in=first_check_in, check_out=last_check_out
            ),
            "check in": first_check_in,
            "check_out": last_check_out,
        }
    return Response(result)
