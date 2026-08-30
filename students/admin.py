from django.contrib import admin
from .models import Course, Student, Room, Attendance, Unit


admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Attendance)
admin.site.register(Unit)