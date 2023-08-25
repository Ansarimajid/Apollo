from django.contrib import messages
from django.shortcuts import (HttpResponse,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import StaffForm, StudentForm, StaffNoteForm, NoteForm, AdminForm
from .models import Student, Staff, CustomUser, Admin, Note, StaffNote , Event
from django.core.files.storage import FileSystemStorage

def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_students = Student.objects.all().count()

    # For Students

    context = {
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_staff': total_staff,
    }
    return render(request, 'hod_template/home_content.html', context)


def add_staff(request):
    staff_form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': staff_form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if staff_form.is_valid():
            first_name = staff_form.cleaned_data.get('first_name')
            last_name = staff_form.cleaned_data.get('last_name')
            email = staff_form.cleaned_data.get('email')
            password = staff_form.cleaned_data.get('password')
            phone_no = staff_form.cleaned_data.get('phone_no')
            alternate_phone_no = staff_form.cleaned_data.get('alternate_phone_no')
            designation = staff_form.cleaned_data.get('designation')
            mon_sal = staff_form.cleaned_data.get('mon_sal')
            year_sal = staff_form.cleaned_data.get('year_sal')
            address = staff_form.cleaned_data.get('address')
            subject_expertise_queryset = staff_form.cleaned_data.get('subject_expertise')
            entitled_el = staff_form.cleaned_data.get('entitled_el')
            form_copy = request.FILES.get("form_copy")
            date_of_birth = staff_form.cleaned_data.get('date_of_birth')
            work_time_start = staff_form.cleaned_data.get('work_time_start')
            work_time_end = staff_form.cleaned_data.get('work_time_end')
            work_day_from = staff_form.cleaned_data.get('work_day_from')
            work_day_to = staff_form.cleaned_data.get('work_day_to')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2,
                    first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)

                staff, created = Staff.objects.get_or_create(
                    admin_id=user.id,
                    defaults={'phone_no': phone_no,
                              'alternate_phone_no': alternate_phone_no,
                              'designation': designation,
                              'mon_sal': mon_sal, 'year_sal': year_sal,
                              'address' : address,
                                'subject_expertise' :subject_expertise_queryset,
                                'entitled_el' :entitled_el,
                                'form_copy': form_copy,
                                'date_of_birth' :date_of_birth,
                                'work_time_start' :work_time_start,
                                'work_time_end' :work_time_end,
                                'work_day_from' :work_day_from,
                                'work_day_to' :work_day_to}
                )

                if not created:
                    staff.phone_no = phone_no
                    staff.alternate_phone_no = alternate_phone_no
                    staff.designation = designation
                    staff.mon_sal = mon_sal
                    staff.year_sal = year_sal
                    staff.address = address
                    staff.subject_expertise.set(subject_expertise_queryset)
                    staff.entitled_el = entitled_el
                    staff.form_copy = form_copy
                    staff.date_of_birth = date_of_birth
                    staff.work_time_start = work_time_start
                    staff.work_time_end = work_time_end
                    staff.work_day_from = work_day_from
                    staff.work_day_to = work_day_to
                    staff.save()

                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))

        else:
            messages.error(request, "Please fulfill all requirements")
    # print(request.POST)
    return render(request, 'hod_template/add_staff_template.html', context)


def add_student(request):
    student_form = StudentForm(request.POST or None,request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student'}
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            email = student_form.cleaned_data.get('email')
            password = student_form.cleaned_data.get('password')
            phone_no = student_form.cleaned_data.get('phone_no')
            alternate_phone_no = \
                student_form.cleaned_data.get('alternate_phone_no')
            board = student_form.cleaned_data.get('board')
            stream = student_form.cleaned_data.get('stream')
            grade = student_form.cleaned_data.get('grade')
            admission_form_copy = request.FILES.get("admission_form_copy")
            school_name = student_form.cleaned_data.get("school_name")
            date_of_birth = student_form.cleaned_data.get("date_of_birth")
            date_of_admission = student_form.cleaned_data.get("date_of_admission")
            gender = student_form.cleaned_data.get("gender")
            handed = student_form.cleaned_data.get("handed")
            batch_time = student_form.cleaned_data.get("batch_time")
            father_name = student_form.cleaned_data.get("father_name")
            father_occupation = student_form.cleaned_data.get("father_occupation")
            mother_name = student_form.cleaned_data.get("mother_name")
            mother_occupation  = student_form.cleaned_data.get("mother_occupation")
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            addmission_form_fees_paid = student_form.cleaned_data.get("addmission_form_fees_paid")

            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3,
                    first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                student, created = Student.objects.get_or_create(
                    admin_id=user.id,
                    defaults={'phone_no': phone_no,
                              'alternate_phone_no': alternate_phone_no,
                              'board': board, 'stream': stream, 'grade': grade ,
                              'admission_form_copy': admission_form_copy,
                                'school_name': school_name,
                                'date_of_birth': date_of_birth,
                                'date_of_admission': date_of_admission,
                                'gender': gender,
                                'handed': handed,
                                'batch_time': batch_time,
                                'father_name': father_name,
                                'father_occupation': father_occupation,
                                'mother_name': mother_name,
                                'mother_occupation': mother_occupation,
                                'addmission_form_fees_paid': addmission_form_fees_paid }
                )
                if not created:
                    # Update the existing student record
                    student.phone_no = phone_no
                    student.alternate_phone_no = alternate_phone_no
                    student.board = board
                    student.stream = stream
                    student.grade = grade
                    student.admission_form_copy = admission_form_copy
                    student.school_name = school_name
                    student.date_of_birth = date_of_birth
                    student.date_of_admission = date_of_admission
                    student.gender = gender
                    student.handed = handed
                    student.batch_time = batch_time
                    student.father_name = father_name
                    student.father_occupation = father_occupation
                    student.mother_name = mother_name
                    student.mother_occupation = mother_occupation
                    student.addmission_form_fees_paid = addmission_form_fees_paid
                    student.save()

                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_student_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Staff'
    }
    return render(request, "hod_template/manage_staff.html", context)


def manage_student(request):
    students = Student.objects.all()
    context = {
        'students': students,
        'page_title': 'Manage Students'
    }

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        payment_status = request.POST.get('payment_status')

        try:
            student = Student.objects.get(pk=student_id)
            student.payment_status = payment_status
            student.save()
            messages.success(request, 'Payment status updated successfully.')
        except Student.DoesNotExist:
            messages.error(request, 'Error updating payment status.')

    return render(request, "hod_template/manage_student.html", context)


def change_payment_status(request, student_id):
    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')
        try:
            student = Student.objects.get(pk=student_id)
            student.payment_status = payment_status
            student.save()
            messages.success(request, 'Payment status updated successfully.')
        except Student.DoesNotExist:
            messages.error(request, 'Error updating payment status.')

    return redirect('manage_student')


def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_note')
    else:
        form = NoteForm()
    return render(request, 'hod_template/upload_note.html',
                  {'page_title': 'Upload Notes', 'form': form})


def upload_staff_note(request):
    if request.method == 'POST':
        form = StaffNoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_staff_note')
    else:
        form = StaffNoteForm()
    return render(request, 'hod_template/upload_staff_note.html',
                  {'page_title': 'Upload Staff Notes', 'form': form})


def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': 'Edit Staff'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password') or None
            phone_no = form.cleaned_data.get('phone_no')
            alternate_phone_no = form.cleaned_data.get('alternate_phone_no')
            designation = form.cleaned_data.get('designation')
            mon_sal = form.cleaned_data.get('mon_sal')
            year_sal = form.cleaned_data.get('year_sal')
            address = form.cleaned_data.get('address')
            subject_expertise_queryset = form.cleaned_data.get('subject_expertise')
            entitled_el = form.cleaned_data.get('entitled_el')
            form_copy = request.FILES.get("form_copy")
            date_of_birth = form.cleaned_data.get('date_of_birth')
            work_time_start = form.cleaned_data.get('work_time_start')
            work_time_end = form.cleaned_data.get('work_time_end')
            work_day_from = form.cleaned_data.get('work_day_from')
            work_day_to = form.cleaned_data.get('work_day_to')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password is not None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                staff.phone_no = phone_no
                staff.alternate_phone_no = alternate_phone_no
                staff.designation = designation
                staff.mon_sal = mon_sal
                staff.year_sal = year_sal
                staff.address = address
                staff.subject_expertise.set(subject_expertise_queryset)
                staff.entitled_el = entitled_el
                staff.form_copy = form_copy
                staff.date_of_birth = date_of_birth
                staff.work_time_start = work_time_start
                staff.work_time_end = work_time_end
                staff.work_day_from = work_day_from
                staff.work_day_to = work_day_to
                user.save()
                staff.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        return render(request, "hod_template/edit_staff_template.html",
                      context)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'student_id': student_id,
        'page_title': 'Edit Student'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password') or None
            phone_no = form.cleaned_data.get('phone_no')
            alternate_phone_no = form.cleaned_data.get('alternate_phone_no')
            board = form.cleaned_data.get('board')
            stream = form.cleaned_data.get('stream')
            grade = form.cleaned_data.get('grade')
            admission_form_copy = request.FILES.get("admission_form_copy")
            school_name = form.cleaned_data.get("school_name")
            date_of_birth = form.cleaned_data.get("date_of_birth")
            date_of_admission = form.cleaned_data.get("date_of_admission")
            gender = form.cleaned_data.get("gender")
            handed = form.cleaned_data.get("handed")
            batch_time = form.cleaned_data.get("batch_time")
            father_name = form.cleaned_data.get("father_name")
            father_occupation = form.cleaned_data.get("father_occupation")
            mother_name = form.cleaned_data.get("mother_name")
            mother_occupation  = form.cleaned_data.get("mother_occupation")
            passport = request.FILES.get('profile_pic') or None
            addmission_form_fees_paid = form.cleaned_data.get("addmission_form_fees_paid")

            try:
                user = CustomUser.objects.get(id=student.admin.id)
                user.username = username
                user.email = email
                if password is not None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                student.phone_no = phone_no
                student.alternate_phone_no = alternate_phone_no
                student.board = board
                student.stream = stream
                student.grade = grade
                student.admission_form_copy = admission_form_copy
                student.school_name = school_name
                student.date_of_birth = date_of_birth
                student.date_of_admission = date_of_admission
                student.gender = gender
                student.handed = handed
                student.batch_time = batch_time
                student.father_name = father_name
                student.father_occupation = father_occupation
                student.mother_name = mother_name
                student.mother_occupation = mother_occupation
                student.addmission_form_fees_paid = addmission_form_fees_paid
                user.save()
                student.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_student_template.html",
                      context)


def edit_notes(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    form = NoteForm(request.POST or None, request.FILES or None, instance=note)
    if request.method == 'POST':
        if form.is_valid():
            # Check if a new file is uploaded
            if 'file' not in request.FILES:
                form.cleaned_data['file'] = note.file

            form.save()
            messages.success(request, "Note updated successfully")
            return redirect(reverse('edit_notes', args=[note_id]))
        else:
            messages.error(request, "Please fill the form properly.")
    return render(request, 'hod_template/edit_notes.html',
                  {'form': form, 'note': note, 'page_title': 'Edit Notes'})


def manage_notes(request):
    all_notes = Note.objects.all()
    context = {
        'all_notes': all_notes,
        'page_title': 'Manage Notes'
    }
    return render(request, 'hod_template/manage_notes.html', context)


def delete_notes(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    messages.success(request, "Note deleted successfully!")
    return redirect('manage_notes')


def edit_staff_notes(request, note_id):
    note = get_object_or_404(StaffNote, id=note_id)
    form = StaffNoteForm(request.POST or None, request.FILES or None,
                         instance=note)

    # Exclude 'shared_with' field from form validation if not selected
    form.fields['shared_with'].required = False

    if request.method == 'POST':
        if form.is_valid():
            # Check if a new file is uploaded
            if 'file' not in request.FILES:
                form.cleaned_data['file'] = note.file

            # Save the form without committing to the database
            staff_note = form.save(commit=False)

            # Clear the existing shared_with relationships
            staff_note.shared_with.clear()

            # Add the selected shared_with staff
            shared_with_ids = request.POST.getlist('shared_with')
            shared_with_staff = Staff.objects.filter(id__in=shared_with_ids)
            staff_note.shared_with.set(shared_with_staff)

            # Save the staff note with updated shared_with relationships
            staff_note.save()

            messages.success(request, "Staff note updated successfully")
            return redirect(reverse('edit_staff_notes', args=[note_id]))
        else:
            messages.error(request, "Please fill the form properly.")
    return render(request, 'hod_template/edit_staff_notes.html',
                  {'form': form, 'note': note, 'page_title': 'Edit Notes'})


def manage_staff_notes(request):
    all_notes = StaffNote.objects.all()
    context = {
        'all_notes': all_notes,
        'page_title': 'Manage Staff Notes'
    }
    return render(request, 'hod_template/manage_staff_notes.html', context)


def delete_staff_notes(request, note_id):
    note = get_object_or_404(StaffNote, id=note_id)
    note.delete()
    messages.success(request, "Staff note deleted successfully!")
    return redirect('manage_staff_notes')


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponse(False)


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password is not None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, staff__id=staff_id)
    staff.delete()
    messages.success(request, "Staff deleted successfully!")
    return redirect(reverse('manage_staff'))


def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))


from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm

def event_list(request):
    events = Event.objects.all()
    return render(request, 'hod_template/event_list.html', {'events': events ,'page_title': 'Event List'})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'hod_template/add_event.html', {'form': form, 'page_title': 'Add Event'})

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'hod_template/edit_event.html', {'form': form, 'event_id': event_id,'page_title': 'Edit Event'})


def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect(reverse('event_list'))


from calendar import HTMLCalendar
from datetime import datetime
from django.views.generic import TemplateView
from .models import Event

from calendar import HTMLCalendar
from datetime import datetime
from django.views.generic import TemplateView
from .models import Event

class MyHTMLCalendar(HTMLCalendar):
    def __init__(self, events, user):
        super().__init__()  # Call super() with no arguments
        self.events = self.group_events_by_day(events)
        self.user = user

    def group_events_by_day(self, events):
        events_by_day = {}
        for event in events:
            day = event.date.day
            if day in events_by_day:
                events_by_day[day].append(event)
            else:
                events_by_day[day] = [event]
        return events_by_day

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # Empty cell for days not in this month

        events = self.events.get(day, [])
        today = datetime.now().day

        if day == today and not events:  # If it's today and there are no events
            return '<td class="today">%d</td>' % day
        elif day == today or events:  # If it's today or there are events
            return '<td class="event">%d</td>' % day
        else:  # For other days without events
            return '<td>%d</td>' % day

from datetime import datetime, timedelta
from django.db.models import Q
class CalendarView(TemplateView):
    template_name = 'hod_template/calendar.html'

    def get_filtered_events(self):
        user = self.request.user
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=1, month=today.month + 1) - timedelta(days=1)

        if user.is_superuser:
            return Event.objects.filter(date__range=[start_of_month, end_of_month]).order_by('date')
        elif user.staff:
            return Event.objects.filter()
        elif user.student:
            return Event.objects.filter()
        else:
            return Event.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now().date()
        calendar = MyHTMLCalendar(self.get_filtered_events(), self.request.user).formatmonth(today.year, today.month)
        events = Event.objects.filter(date__year=today.year, date__month=today.month)
        context['calendar'] = calendar
        context['today'] = today
        context['events'] = events
        context['page_title'] = 'Academic Calendar'
        return context




