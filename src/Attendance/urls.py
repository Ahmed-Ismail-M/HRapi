from django.urls import path
from Attendance.views.EmpView import RegisterAPI

urlpatterns = [path("api/v1/register", RegisterAPI.as_view(), name="register"),
]
