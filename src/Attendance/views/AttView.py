from rest_framework import generics
from datetime import datetime
from Attendance.models import Attendance
from Attendance.serializers.AttSerializer import (
    AttendanceSerializer,
    AttendancesSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from Attendance.middleware import auth_required, allowed_users
from rest_framework.decorators import api_view
from Attendance.datastore.att_data_store import (
    get_daily_report_by_user,
    get_daily_index_by_user,
    get_all_attendances,
)

from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class Create(generics.GenericAPIView):

    serializer_class = AttendanceSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

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
def daily_index_by_user(request):
    return Response(get_daily_index_by_user(user_id=request.user.id))


@api_view()
def daily_report_by_user(request):
    return Response(get_daily_report_by_user(user_id=request.user.id))


class Index(generics.ListAPIView):
    serializer_class = AttendancesSerializer

    def get_queryset(self):
        queryset = Attendance.objects.all()
        return queryset

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Admin"]))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
