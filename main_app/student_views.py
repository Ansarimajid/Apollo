from django.shortcuts import get_object_or_404, render
from .forms import StudentEditForm
from .models import Note, Student
from django.http import HttpResponse


def view_notes(request):
    user = request.user  # Get the current user
    if user.is_authenticated and user.user_type == '3':
        student = user.student  # Get the student instance
        grade = student.grade  # Get the grade of the student
        notes = Note.objects.filter(grade=grade)
        return render(request, 'student_template/view_notes.html',
                      {'page_title': 'View Notes', 'notes': notes})
    else:
        # Handle the case if the user is not authenticated or not a student
        return HttpResponse("You are not authorized to view this page.")


def student_home(request):
    context = {
        'page_title': 'Student Homepage'
    }
    return render(request, 'student_template/home_content.html', context)


def student_view_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(instance=student)
    context = {
        'form': form,
        'page_title': 'View Profile'
    }
    return render(request, "student_template/student_view_profile.html",
                  context)

from calendar import HTMLCalendar
from datetime import datetime
from django.views.generic import TemplateView
from .models import Event
from .hod_views import MyHTMLCalendar , CalendarView
from datetime import datetime, timedelta

class CalendarViewStudent(CalendarView):
    template_name = 'hod_template/calendar.html'

    def get_filtered_events(self):
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=1, month=today.month + 1) - timedelta(days=1)
        user = self.request.user
        print(user)
        return Event.objects.filter(date__range=[start_of_month, end_of_month], grade=user.student.grade, board=user.student.board)
