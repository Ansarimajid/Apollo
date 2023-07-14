from django.urls import path

from . import hod_views, staff_views, student_views, views
from .hod_views import CalendarView
from .staff_views import CalendarViewStaff
from .student_views import CalendarViewStudent

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add/", hod_views.add_staff, name='add_staff'),
    path("admin_view_profile/", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability/", hod_views.check_email_availability,
         name="check_email_availability"),
    path("student/add/", hod_views.add_student, name='add_student'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),
    path("staff/edit/<int:staff_id>/", hod_views.edit_staff,
         name='edit_staff'),
    path("staff/delete/<int:staff_id>/", hod_views.delete_staff,
         name='delete_staff'),
    path("student/delete/<int:student_id>/", hod_views.delete_student,
         name='delete_student'),
    path("student/edit/<int:student_id>/", hod_views.edit_student,
         name='edit_student'),
    path('payment-required/', views.payment_required, name='payment_required'),
    path('changestatus/<int:student_id>/', hod_views.change_payment_status,
         name='change_payment_status'),
    path('admin/upload_notes/', hod_views.upload_note, name='upload_note'),
    path('admin/upload_staff_notes/', hod_views.upload_staff_note,
         name='upload_staff_note'),
    path('admin/edit_notes/<int:note_id>/', hod_views.edit_notes,
         name='edit_notes'),
    path('staff/edit_staff_notes/<int:note_id>/', hod_views.edit_staff_notes,
         name='edit_staff_notes'),
    path('staff/manage_staff_notes/', hod_views.manage_staff_notes,
         name='manage_staff_notes'),
    path('staff/delete_staff_notes/<int:note_id>/',
         hod_views.delete_staff_notes, name='delete_staff_notes'),
    path('notes/edit/<int:note_id>/', hod_views.edit_notes, name='edit_notes'),
    path('notes/manage/', hod_views.manage_notes, name='manage_notes'),
    path('notes/delete/<int:note_id>/', hod_views.delete_notes,
         name='delete_notes'),
     path('calendar/', CalendarView.as_view(), name='calendar'),
     path('events/', hod_views.event_list, name='event_list'),
    path('events/add/', hod_views.add_event, name='add_event'),
    path('events/delete/<int:event_id>/', hod_views.delete_event, name='delete_event'),
    path('events/edit/<int:event_id>/', hod_views.edit_event, name='edit_event'),

    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path('staff/view_staff_notes/', staff_views.view_staff_notes,
         name='view_staff_notes'),
          path('staff_calendar/', CalendarViewStaff.as_view(), name='calendarstaff'),

    # Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/view/profile/", student_views.student_view_profile,
         name='student_view_profile'),
    path('student/view_notes/', student_views.view_notes, name='view_notes'),
     path('student_calendar/', CalendarViewStudent.as_view(), name='calendarstudent'),
]
