from django.db import models
from django.contrib.auth.models import AbstractUser

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
    date = models.DateField
# Create your models here.
