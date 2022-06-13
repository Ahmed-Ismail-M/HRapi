from django.urls import path
from Attendance.views.EmpView import RegisterAPI, LoginAPI
from Attendance.views.AttView import AddAttendance

urlpatterns = [path("api/v1/register", RegisterAPI.as_view(), name="register"),
               path("api/v1/login", LoginAPI.as_view(), name="login"),
               path("api/v1/attendance", AddAttendance.as_view(), name="add_att"),
               ]
