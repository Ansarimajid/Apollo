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

class CalendarViewStudent(TemplateView):
    template_name = 'hod_template/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now().date()
        calendar = HTMLCalendar().formatmonth(today.year, today.month)
        events = Event.objects.filter(date__year=today.year, date__month=today.month)
        highlighted_calendar = self.apply_highlighting(calendar, today.day, [event.date.day for event in events])
        context['calendar'] = highlighted_calendar
        context['events'] = events
        context['page_title'] = 'Calendar'
        return context
    
    def apply_highlighting(self, cal, today, events_dates):
        highlighted_cal = cal.replace('>%s</td>' % today, ' class="today">%s</td>' % today)
        for event_date in events_dates:
            highlighted_cal = highlighted_cal.replace('>%s</td>' % event_date, ' class="event">%s</td>' % event_date)
        return highlighted_cal