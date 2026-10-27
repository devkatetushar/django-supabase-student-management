from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Student

def home(request):
    return render(request, "school/home.html")

def student_login(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect("student_dashboard")
        error = "Login failed. Check your username and password, or contact the administrator."
    return render(request, "school/student_login.html", {"error": error})

@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect("/admin/")
    student = Student.objects.filter(user=request.user).first()
    return render(request, "school/student_dashboard.html", {"student": student})

@require_POST
def student_logout(request):
    logout(request)
    return redirect("home")

def staff_required(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(staff_required, login_url="/admin/login/")
def student_list(request):
    students = Student.objects.all().order_by("id")
    return render(request, "school/student_manage.html", {"students": students})

@user_passes_test(staff_required, login_url="/admin/login/")
def student_create(request):
    if request.method != "POST":
        return redirect("student_manage")
    data = _form_data(request)
    if not _valid(data):
        messages.error(request, "Please complete all required fields and enter a valid age.")
        return redirect("student_manage")
    try:
        Student.objects.create(**data)
        messages.success(request, "Student added successfully.")
    except IntegrityError:
        messages.error(request, "That roll number or email is already in use.")
    return redirect("student_manage")

@user_passes_test(staff_required, login_url="/admin/login/")
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method != "POST":
        return render(request, "school/student_manage.html", {
            "students": Student.objects.all().order_by("id"), "edit_student": student
        })
    data = _form_data(request)
    if not _valid(data):
        messages.error(request, "Please complete all required fields and enter a valid age.")
        return redirect("student_manage")
    for field, value in data.items():
        setattr(student, field, value)
    try:
        student.save()
        messages.success(request, "Student updated successfully.")
    except IntegrityError:
        messages.error(request, "That roll number or email is already in use.")
    return redirect("student_manage")

@require_POST
@user_passes_test(staff_required, login_url="/admin/login/")
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("student_manage")

def _form_data(request):
    return {
        "name": request.POST.get("name", "").strip(),
        "roll_number": request.POST.get("roll_number", "").strip(),
        "email": request.POST.get("email", "").strip(),
        "age": _parse_age(request.POST.get("age", "")),
        "course": request.POST.get("course", "").strip(),
        "address": request.POST.get("address", "").strip(),
    }

def _parse_age(value):
    try:
        age = int(value)
        return age if age >= 0 else None
    except (TypeError, ValueError):
        return None

def _valid(data):
    return bool(data["name"] and data["roll_number"] and data["email"] and data["age"] is not None and data["course"])
