from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "roll_number", "email", "age", "course", "user", "created_at")
    search_fields = ("name", "roll_number", "email", "user__username")
    list_filter = ("course", "age")
    ordering = ("name",)
