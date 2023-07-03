from django.shortcuts import (get_object_or_404, render)
from .forms import *
from .models import *

def view_staff_notes(request):
    notes = StaffNote.objects.all()
    return render(request, 'staff_template/view_staff_notes.html', {'page_title': 'View Notes','notes': notes})


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_students = Student.objects.count()
    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.first_name) + ' ' + str(staff.admin.last_name[0]) ,
        'total_students': total_students,
    }
    return render(request, 'staff_template/home_content.html', context)

def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(instance=staff)
    context = {'form': form, 'page_title': 'View Profile'}
    return render(request, "staff_template/staff_view_profile.html", context)
