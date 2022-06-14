from rest_framework import generics
from datetime import datetime
from Attendance.models import Attendance
from Attendance.serializers.AttSerializer import AttendanceSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from Attendance.middleware import auth_required, allowed_users
from rest_framework.decorators import api_view
from Attendance.datastore.att_data_store import get_daily_report_by_user, get_daily_index_by_user, get_all_attendances

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


class IndexByUser(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.all().filter(emp=self.request.user.id)
        return queryset


@api_view()
def daily_index(request):
    return Response(get_daily_index_by_user(user_id=request.user.id))


@api_view()
def daily_report(request):
    return Response(get_daily_report_by_user(user_id=request.user.id))

@auth_required
@allowed_users(allowed_roles=["Admin"])
def index(request):
    return Response(get_all_attendances())