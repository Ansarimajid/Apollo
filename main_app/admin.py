from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Staff, Student, Note, StaffNote, Event, Board, Grade, Stream

# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Note)
admin.site.register(StaffNote)
admin.site.register(Event)
admin.site.register(Board)
admin.site.register(Grade)
admin.site.register(Stream)
