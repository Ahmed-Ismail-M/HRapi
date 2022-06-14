from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class Employee(AbstractUser):
    class Meta:
        verbose_name = "employee"
        verbose_name_plural = 'employees'

class Attendance(models.Model):
    WORKING_HRS = {'in':5, 'out':9}
    emp = models.ForeignKey(
        Employee, on_delete=models.CASCADE,  related_name='employee')
    check_in = models.TimeField(default=None, null=True)
    check_out = models.TimeField(default=None, null=True)
    date = models.DateField(default=date.today)

    @property
    def check_late(self) -> bool:
        if self.check_in> self.WORKING_HRS['in']:
            return True
        return False

    @property
    def check_early_leave(self)-> bool:
        if self.check_out< self.WORKING_HRS['out']:
            return True
        return False