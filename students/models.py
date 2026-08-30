from django.db import models


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Student(models.Model):
    registration_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="students"
    )

    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"

class Room(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    building = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.building} - Room {self.room_number}"


class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    date = models.DateField(auto_now_add=True)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.date}"    

class Unit(models.Model):
    unit_code = models.CharField(max_length=20, unique=True)
    unit_name = models.CharField(max_length=150)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="units"
    )

    def __str__(self):
       return f"{self.unit_code} - {self.course}"