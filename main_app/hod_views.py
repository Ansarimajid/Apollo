from django.contrib import messages
from django.shortcuts import (HttpResponse,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import StaffForm, StudentForm, StaffNoteForm, NoteForm, AdminForm
from .models import Student, Staff, CustomUser, Admin, Note, StaffNote


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
    form = StaffForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            phone_no = form.cleaned_data.get('phone_no')
            alternate_phone_no = form.cleaned_data.get('alternate_phone_no')
            designation = form.cleaned_data.get('designation')
            mon_sal = form.cleaned_data.get('mon_sal')
            year_sal = form.cleaned_data.get('year_sal')
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2,
                    first_name=first_name, last_name=last_name)

                staff, created = Staff.objects.get_or_create(
                    admin_id=user.id,
                    defaults={'phone_no': phone_no,
                              'alternate_phone_no': alternate_phone_no,
                              'designation': designation,
                              'mon_sal': mon_sal, 'year_sal': year_sal}
                )

                if not created:
                    staff.phone_no = phone_no
                    staff.alternate_phone_no = alternate_phone_no
                    staff.designation = designation
                    staff.mon_sal = mon_sal
                    staff.year_sal = year_sal
                    staff.save()

                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))

        else:
            messages.error(request, "Please fulfill all requirements")
    print(request.POST)
    return render(request, 'hod_template/add_staff_template.html', context)


def add_student(request):
    student_form = StudentForm(request.POST or None)
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
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3,
                    first_name=first_name, last_name=last_name)
                student, created = Student.objects.get_or_create(
                    admin_id=user.id,
                    defaults={'phone_no': phone_no,
                              'alternate_phone_no': alternate_phone_no,
                              'board': board, 'stream': stream, 'grade': grade}
                )
                if not created:
                    # Update the existing student record
                    student.phone_no = phone_no
                    student.alternate_phone_no = alternate_phone_no
                    student.board = board
                    student.stream = stream
                    student.grade = grade
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
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password is not None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                staff.phone_no = phone_no
                staff.alternate_phone_no = alternate_phone_no
                staff.designation = designation
                staff.mon_sal = mon_sal
                staff.year_sal = year_sal
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
            try:
                user = CustomUser.objects.get(id=student.admin.id)
                user.username = username
                user.email = email
                if password is not None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                student.phone_no = phone_no
                student.alternate_phone_no = alternate_phone_no
                student.board = board
                student.stream = stream
                student.grade = grade
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
                custom_user = admin.admin
                if password is not None:
                    custom_user.set_password(password)
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
