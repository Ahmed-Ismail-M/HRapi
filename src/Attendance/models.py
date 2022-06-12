from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
class User(AbstractUser):
    pass
class Employee(User):
    class Meta:
        verbose_name = "employee"
        verbose_name_plural = 'employees'
class Attendance(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE,  related_name='employee')
    check_in = models.TimeField()
    check_out = models.TimeField()
    date = models.DateField(default=date.today)
# Create your models here.
