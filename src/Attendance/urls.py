from django.urls import path
from Attendance.views.EmpView import RegisterAPI, LoginAPI
from Attendance.views.AttView import Create, IndexByUser, daily_index, daily_report, Index

urlpatterns = [path("api/v1/register", RegisterAPI.as_view(), name="register"),
               path("api/v1/login", LoginAPI.as_view(), name="login"),
               path("api/v1/attendance", Create.as_view(), name="add_att"),
               path("api/v1/attendances", IndexByUser.as_view(), name="get_atts"),
               path("api/v1/daily/attendances", daily_index, name="daily_index"),
               path("api/v1/report/attendances", daily_report, name="daily_report"),
               path("api/v1/allattendances", Index.as_view(), name="index"),
               ]
               
