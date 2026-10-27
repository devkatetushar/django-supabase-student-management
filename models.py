from django.conf import settings
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="student_profile",
        help_text="Optional Django login account for this student.",
    )
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    course = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"
