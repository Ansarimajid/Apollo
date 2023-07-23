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


class Student(models.Model):
    BOARD_CHOICES = (
        ('CBSE', 'CBSE'),
        ('ICSE', 'ICSE'),
        ('State Board', 'State Board'),
        # Add more choices as needed
    )

    STREAM_CHOICES = (
        ('Science', 'Science'),
        ('Commerce', 'Commerce'),
        ('Arts', 'Arts'),
        # Add more choices as needed
    )

    GRADE_CHOICES = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
        ('6th', '6th'),
        ('7th', '7th'),
        ('8th', '8th'),
        ('9th', '9th'),
        ('10th', '10th'),
        ('11th', '11th'),
        ('12th', '12th'),
        # Add more choices as needed
    )

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
        # Add more cho
    )

    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=20)
    alternate_phone_no = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    handed = models.CharField(max_length=10, choices=HANDED_CHOICES)
    board = models.CharField(max_length=100, choices=BOARD_CHOICES)
    stream = models.CharField(max_length=100, choices=STREAM_CHOICES)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    admission_form_copy = models.FileField(upload_to='admission_forms/',default="admission_forms/default.png")
    school_name = models.CharField(max_length=100, default="School Name")
    date_of_birth = models.DateField(default="2000-01-01")
    date_of_admission = models.DateField(default="2000-01-01")
    batch_time = models.TimeField(default="00:00:00")
    father_name = models.CharField(max_length=100, default="Father Name")
    father_occupation = models.CharField(max_length=100, default="Father Occupation")
    mother_name = models.CharField(max_length=100, default="Mother Name")
    mother_occupation = models.CharField(max_length=100, default="Mother Occupation")

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name



from django.core.validators import FileExtensionValidator
from django.db import models

class Staff(models.Model):
    DESIGNATION_CHOICES = (
        ('Assistant', 'Assistant'),
        ('Teacher', 'Teacher'),
        ('Faculty', 'Faculty'),
    )
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    alternate_phone_no = models.CharField(max_length=20)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES)
    mon_sal = models.IntegerField(null=True, blank=True)
    year_sal = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, default="")
    subject_expertise = models.CharField(max_length=100, default="")
    entitled_el = models.IntegerField(default=0)
    al_copy = models.FileField(upload_to='al_copies/', default="")
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
    grade = models.CharField(max_length=10, choices=Student.GRADE_CHOICES,
                             default=1)

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

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    shared_with_staff = models.ManyToManyField(Staff, blank=True)
    board = models.CharField(max_length=20, choices=Student.BOARD_CHOICES, default=1, blank=True, null=True)
    grade = models.CharField(max_length=20, choices=Student.GRADE_CHOICES, default=1, blank=True, null=True)

    def __str__(self):
        return self.title

