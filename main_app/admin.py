from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Staff, Student

# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Student)
