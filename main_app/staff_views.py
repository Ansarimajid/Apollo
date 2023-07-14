from django.shortcuts import get_object_or_404, render
from .forms import StaffEditForm
from .models import Staff, Student
from django.http import HttpResponse


def view_staff_notes(request):
    user = request.user  # Get the current user
    if user.is_authenticated and user.user_type == '2':
        staff = user.staff  # Get the staff instance
        notes = staff.staffnote_set.all()
        return render(request, 'staff_template/view_staff_notes.html',
                      {'page_title': 'View Notes', 'notes': notes})
    else:
        # Handle the case if the user is not authenticated or not a staff
        return HttpResponse("You are not authorized to view this page.")


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_students = Student.objects.count()
    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.first_name) +
        ' ' + str(staff.admin.last_name[0]),
        'total_students': total_students,
    }
    return render(request, 'staff_template/home_content.html', context)


def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(instance=staff)
    context = {
        'form': form,
        'page_title': 'View Profile'
    }
    return render(request, "staff_template/staff_view_profile.html", context)

from calendar import HTMLCalendar
from datetime import datetime
from django.views.generic import TemplateView
from .models import Event

class CalendarViewStaff(TemplateView):
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