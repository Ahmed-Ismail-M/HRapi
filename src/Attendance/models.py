from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime, time


class Employee(AbstractUser):
    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"


class Attendance(models.Model):
    WORKING_HRS = {
        "in": time(hour=9, minute=0, second=0, microsecond=0) ,
        "out":  time(hour=5, minute=0, second=0, microsecond=0) ,
    }
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee")
    check_in = models.TimeField(default=None, null=True)
    check_out = models.TimeField(default=None, null=True)
    date = models.DateField(default=date.today)

    @classmethod
    def check_late(cls, check_in: time) -> bool:
        if check_in > cls.WORKING_HRS["in"]:
            return True
        return False

    @classmethod
    def check_early_leave(cls, check_out: time) -> bool:
        if check_out < cls.WORKING_HRS["out"]:
            return True
        return False
