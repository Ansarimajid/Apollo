# forms.py

from django import forms
from .models import Note, StaffNote, CustomUser, Student, Admin, Staff, Event, Board, Stream, Grade, Subject
from django.forms.widgets import CheckboxSelectMultiple

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

        if 'subject_expertise' in self.fields:
            self.fields['subject_expertise'].widget.attrs['class'] = 'checkbox-se'



class NoteForm(forms.ModelForm):
    grade = forms.ModelMultipleChoiceField(
        queryset=Grade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    board = forms.ModelMultipleChoiceField(
        queryset=Board.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    stream = forms.ModelMultipleChoiceField(
        queryset=Stream.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    
    class Meta:
        model = Note
        fields = ('title', 'description', 'file', 'grade', 'board', 'stream')


class NoteEditForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'description', 'file', 'grade')


class StaffNoteForm(forms.ModelForm):
    shared_with = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = StaffNote
        fields = ('title', 'description', 'file', 'shared_with')


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError("The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There have been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password','profile_pic']


class StudentForm(CustomUserForm):
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES)
    handed = forms.ChoiceField(choices=Student.HANDED_CHOICES)
    addmission_form_fees_paid = forms.ChoiceField(choices=Student.FEE_PAID)
    board = forms.ModelChoiceField(queryset=Board.objects.all())
    stream = forms.ModelChoiceField(queryset=Stream.objects.all())
    grade = forms.ModelChoiceField(queryset=Grade.objects.all())
    admission_form_copy = forms.FileField(required=False)
    school_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_admission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    batch_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    father_name = forms.CharField(max_length=100)
    father_occupation = forms.CharField(max_length=100)
    mother_name = forms.CharField(max_length=100)
    mother_occupation = forms.CharField(max_length=100)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + [
            'phone_no',
            'alternate_phone_no',
            'gender',
            'handed',
            'board',
            'stream',
            'grade',
            'admission_form_copy',
            'school_name',
            'date_of_birth',
            'date_of_admission',
            'batch_time',
            'father_name',
            'father_occupation',
            'mother_name',
            'mother_occupation',
            'addmission_form_fees_paid'
        ]
class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop('attrs', {})
        attrs['class'] = 'checkbox-se'  # Add your custom class here
        super().__init__(*args, attrs=attrs, **kwargs)

class StaffForm(CustomUserForm):
    phone_no = forms.CharField(max_length=20)
    alternate_phone_no = forms.CharField(max_length=20)
    designation = forms.ChoiceField(choices=Staff.DESIGNATION_CHOICES)
    mon_sal = forms.IntegerField()
    year_sal = forms.IntegerField()
    address = forms.CharField(max_length=100)
    subject_expertise = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    entitled_el = forms.IntegerField()
    form_copy = forms.FileField(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    work_time_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    work_time_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    work_day_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) 
    work_day_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + [
            'phone_no',
            'alternate_phone_no',
            'designation',
            'mon_sal',
            'year_sal',
            'address',
            'subject_expertise',
            'entitled_el',
            'form_copy',
            'date_of_birth',
            'work_time_start',
            'work_time_end',
            'work_day_from',
            'work_day_to',
        ]


class AdminForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffEditForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + [
            'phone_no',
            'alternate_phone_no',
            'designation',
            'mon_sal',
            'year_sal',
            'address',
            'subject_expertise',
            'entitled_el',
            'form_copy',
            'date_of_birth',
            'work_time_start',
            'work_time_end',
            'work_day_from',
            'work_day_to',
        ]


class StudentEditForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + [  
            'phone_no',
            'alternate_phone_no',
            'gender',
            'handed',
            'board',
            'stream',
            'admission_form_copy',
            'school_name',
            'date_of_birth',
            'date_of_admission',
            'batch_time',
            'father_name',
            'father_occupation',
            'mother_name',
            'mother_occupation',
        ]


class EventForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.TextInput()
    shared_with_staff = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    select_all_staff = forms.BooleanField(required=False, initial=False)

    grade = forms.ModelMultipleChoiceField(
        queryset=Grade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    board = forms.ModelMultipleChoiceField(
        queryset=Board.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    # Additional field for "Select All" checkbox
    select_all_grades_and_boards = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'select-all-grades-boards'})
    )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['shared_with_staff'].widget.attrs['class'] = 'select-all-staff'
        self.fields['select_all_staff'].widget.attrs['class'] = 'select-all-staff-checkbox'

        if self.data.get('select_all_staff') == 'on':
            self.fields['shared_with_staff'].initial = list(Staff.objects.values_list('id', flat=True))

    def clean(self):
        cleaned_data = super().clean()
        select_all_staff = cleaned_data.get('select_all_staff')
        if select_all_staff:
            cleaned_data['shared_with_staff'] = list(Staff.objects.values_list('id', flat=True))

        select_all_grades_and_boards = cleaned_data.get('select_all_grades_and_boards')
        if select_all_grades_and_boards:
            cleaned_data['grade'] = list(Grade.objects.values_list('id', flat=True))
            cleaned_data['board'] = list(Board.objects.values_list('id', flat=True))

        return cleaned_data

    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'shared_with_staff', 'select_all_staff', 'grade', 'board']
