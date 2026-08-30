from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Student, Course, Room, Attendance, Unit

def home(request):
    student_count = Student.objects.count()
    course_count = Course.objects.count()
    unit_count = Unit.objects.count()
    attendance_count = Attendance.objects.count()

    return render(
        request,
        "students/home.html",
        {
            "student_count": student_count,
            "course_count": course_count,
            "unit_count": unit_count,
            "attendance_count": attendance_count,
        }
    )

def register_student(request):

    if request.method == "POST":

        registration_number = request.POST.get("registration_number")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course_id = request.POST.get("course")

        # Check if registration number already exists
        if Student.objects.filter(
            registration_number=registration_number
        ).exists():

            courses = Course.objects.all()

            return render(
                request,
                "students/register_student.html",
                {
                    "courses": courses,
                    "error": "A student with this registration number already exists."
                }
            )

        # Check if email already exists
        if Student.objects.filter(email=email).exists():

            courses = Course.objects.all()

            return render(
                request,
                "students/register_student.html",
                {
                    "courses": courses,
                    "error": "A student with this email address already exists."
                }
            )

        # Save the new student
        Student.objects.create(
            registration_number=registration_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            course_id=course_id
        )

        return redirect("home")

    courses = Course.objects.all()

    return render(
        request,
        "students/register_student.html",
        {"courses": courses}
    )

def student_list(request):
    students = Student.objects.select_related("course").prefetch_related(
        "attendance_records__room"
    ).all()

    return render(
        request,
        "students/student_list.html",
        {"students": students}
    )

def student_detail(request, student_id):
    student = Student.objects.select_related("course").get(id=student_id)

    attendance_records = student.attendance_records.select_related(
        "room"
    ).order_by("-date", "-entry_time")

    units = student.course.units.all().order_by("unit_code")

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "attendance_records": attendance_records,
            "units": units,
        }
    )
def attendance(request):

    if request.method == "POST":

        student_id = request.POST.get("student")
        room_id = request.POST.get("room")

        student = Student.objects.get(id=student_id)
        room = Room.objects.get(id=room_id)

        # Check if the student is already inside
        active_attendance = Attendance.objects.filter(
            student=student,
            exit_time__isnull=True
        ).first()

        if active_attendance:
            return render(
                request,
                "students/attendance.html",
                {
                    "students": Student.objects.all(),
                    "rooms": Room.objects.all(),
                    "error": (
                        f"{student.first_name} {student.last_name} "
                        "is already marked as present."
                    )
                }
            )

        # Create a new attendance record
        Attendance.objects.create(
            student=student,
            room=room,
            entry_time=timezone.now()
        )

        return redirect("student_list")

    students = Student.objects.all()
    rooms = Room.objects.all()

    return render(
        request,
        "students/attendance.html",
        {
            "students": students,
            "rooms": rooms
        }
    )

def record_exit(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)

    if attendance.exit_time is None:
        attendance.exit_time = timezone.now()
        attendance.save()

    return redirect("student_list")   