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
    return(str(check_in-check_out))

class Create(generics.GenericAPIView):

    serializer_class = AttendanceSerializer

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Employee"]))
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
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
        str_date =att.date.strftime('%d/%m/%Y')
        if str_date not in result:
            if att.check_in:
                result[str_date] = {f'In-{stri}': att.check_in}
            if att.check_out:
                result[str_date] = {f'Out-{stri}': att.check_out}
        else:
            if att.check_in:
                result[str_date][f'In-{stri}'] = att.check_in
            if att.check_out:
                result[str_date][f'Out-{stri}'] = att.check_out
                
    # memo_intervals = []
    # for index, att in enumerate(daily_atts):
    #     str_date =att.date.strftime('%d/%m/%Y')
    #     if str_date not in result:
    #         if att.check_in:
    #             memo_check_in = att.check_in
    #         result[str_date] = {'total_hrs': calc_working_hrs(att.check_in, att.check_out)}
    #     else:
    #         result[str_date]['total_hrs']= calc_working_hrs(att.check_in, att.check_out)
    return Response(result)

@api_view()
def DailyReport(request):
    daily_atts = Attendance.objects.all().filter(emp=request.user.id).values_list('date', flat=True).distinct()
    result = {}
    for index, date in enumerate(daily_atts):
        str_date =date.strftime('%d/%m/%Y')
        # get last check in and out
        last_check_in = Attendance.objects.all().filter(
            date=date).latest('check_in').check_in
        last_check_out = Attendance.objects.all().filter(
            date=date).latest('check_out')
        result[str_date] = "Late" if Attendance.check_late(last_check_in) else ""
    return Response(result)