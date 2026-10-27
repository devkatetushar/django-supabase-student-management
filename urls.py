from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("student/login/", views.student_login, name="student_login"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/logout/", views.student_logout, name="student_logout"),
    path("manage/", views.student_list, name="student_manage"),
    path("manage/create/", views.student_create, name="student_create"),
    path("manage/update/<int:pk>/", views.student_update, name="student_update"),
    path("manage/delete/<int:pk>/", views.student_delete, name="student_delete"),
]
