from django.urls import path
from Attendance.views.EmpView import RegisterAPI, LoginAPI
from Attendance.views.AttView import Create, Index, DailyIndex, DailyReport

urlpatterns = [path("api/v1/register", RegisterAPI.as_view(), name="register"),
               path("api/v1/login", LoginAPI.as_view(), name="login"),
               path("api/v1/attendance", Create.as_view(), name="add_att"),
               path("api/v1/attendances", Index.as_view(), name="get_atts"),
               path("api/v1/daily/attendances", DailyIndex, name="daily_index"),
               path("api/v1/report/attendances", DailyReport, name="daily_report"),
               ]
               
