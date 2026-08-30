from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_student, name="register_student"),
    path("students/", views.student_list, name="student_list"),

    path(
        "students/<int:student_id>/",
        views.student_detail,
        name="student_detail"
    ),

    path("attendance/", views.attendance, name="attendance"),

    path(
        "attendance/<int:attendance_id>/exit/",
        views.record_exit,
        name="record_exit"
    ),
]