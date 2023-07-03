from django.shortcuts import (get_object_or_404, render)
from .forms import *
from .models import *

def view_notes(request):
    notes = Note.objects.all()
    return render(request, 'student_template/view_notes.html', {'page_title': 'View Notes','notes': notes})

def student_home(request):
    student = get_object_or_404(Student, admin=request.user)
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
    return render(request, "student_template/student_view_profile.html", context)
