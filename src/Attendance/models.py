from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class Employee(AbstractUser):
    class Meta:
        verbose_name = "employee"
        verbose_name_plural = 'employees'

class Attendance(models.Model):
    class Check(models.TextChoices):
        CHECKIN = 'in'
        CHECKOUT = 'out'
    emp = models.ForeignKey(
        Employee, on_delete=models.CASCADE,  related_name='employee')
    check = models.CharField(max_length=3, choices=Check.choices)
    date = models.DateTimeField(default=date.today)

