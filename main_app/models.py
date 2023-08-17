from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"))

    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    profile_pic = models.ImageField()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_paid_fees(self):
        try:
            student = Student.objects.get(admin=self)
            return student.payment_status
        except Student.DoesNotExist:
            return False

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # new instance being created
        super().save(*args, **kwargs)
        if is_new and self.user_type == '3':
            Student.objects.create(admin=self)  # Create Student instance


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

from django.db import models
from django.core.validators import FileExtensionValidator

from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stream(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        # Add more choices as needed
    )

    HANDED_CHOICES = (
        ('Right', 'Right'),
        ('Left', 'Left'),
        ('Both', 'Both'),
        # Add more choices as needed
    )

    FEE_PAID = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=20)
    alternate_phone_no = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    handed = models.CharField(max_length=10, choices=HANDED_CHOICES)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    admission_form_copy = models.FileField(upload_to='admission_forms/',default="admission_forms/default.png")
    school_name = models.CharField(max_length=100, default="School Name")
    date_of_birth = models.DateField(default="2000-01-01")
    date_of_admission = models.DateField(default="2000-01-01")
    batch_time = models.TimeField(default="00:00:00")
    father_name = models.CharField(max_length=100, default="Father Name")
    father_occupation = models.CharField(max_length=100, default="Father Occupation")
    mother_name = models.CharField(max_length=100, default="Mother Name")
    mother_occupation = models.CharField(max_length=100, default="Mother Occupation")
    addmission_form_fees_paid = models.CharField(max_length=10, choices=FEE_PAID, default="No")

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name

class Staff(models.Model):
    DESIGNATION_CHOICES = (
        ('Helper', 'Helper'),
        ('Faculty/Teacher', 'Faculty/Teacher'),
    )
    SUBJECT_CHOICES = (
        ('Science', 'Science'),
        ('English', 'English'),
        ('Maths', 'Maths'),
        ('Hindi', 'Hindi'),
        ('SST', 'SST'),
        ('EVS', 'EVS'),
        ('ECO/BS/CA', 'ECO/BS/CA'),
        ('Accounts', 'Accounts'),
    )
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    alternate_phone_no = models.CharField(max_length=20)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES)
    mon_sal = models.IntegerField(null=True, blank=True)
    year_sal = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, default="")
    subject_expertise = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    entitled_el = models.IntegerField(default=0)
    form_copy = models.FileField(upload_to='forms/',default="forms/default.png")
    date_of_birth = models.DateField(null=True, blank=True)
    work_time_start = models.TimeField(null=True, blank=True)
    work_time_end = models.TimeField(null=True, blank=True)
    work_day_from = models.DateField(null=True, blank=True)
    work_day_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()


class Note(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='notes/')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                    default=1)
    grade = models.ManyToManyField(Grade, blank=True)
    board = models.ManyToManyField(Board, blank=True)
    stream = models.ManyToManyField(Stream, blank=True)

    def __str__(self):
        return self.title


class StaffNote(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='staff_notes/')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                    default=1)
    shared_with = models.ManyToManyField(Staff)

    def __str__(self):
        return self.title

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    shared_with_staff = models.ManyToManyField(Staff, blank=True)
    board = models.ManyToManyField(Board, blank=True)
    grade = models.ManyToManyField(Grade, blank=True)

    def __str__(self):
        return self.title


