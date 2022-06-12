from django.urls import path
from Attendance.views.EmpView import RegisterAPI
from Attendance.views.AttView import AddAttendance

urlpatterns = [path("api/v1/register", RegisterAPI.as_view(), name="register"),
path("api/v1/attendance", AddAttendance.as_view(), name="add_att"),
]
