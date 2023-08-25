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
from .hod_views import MyHTMLCalendar , CalendarView
from datetime import datetime, timedelta
class CalendarViewStaff(CalendarView):
    template_name = 'hod_template/calendar.html'  # Adjust the template path as needed

    def get_filtered_events(self):
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=1, month=today.month + 1) - timedelta(days=1)
        user = self.request.user
        # print(user)
        # print(user.staff)
        return Event.objects.filter(date__range=[start_of_month, end_of_month],shared_with_staff=user.staff)
    

