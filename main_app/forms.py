from django import forms
from .models import Note, StaffNote, CustomUser, Student, Admin, Staff


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'description', 'file', 'grade')


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

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill" \
                    " this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError("The given email" +
                                            " is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(id=self.instance.pk)\
                .admin.email.lower()
            if dbEmail != formEmail:  # There have been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email" +
                                                " is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']


from django import forms
from .models import Student

class StudentForm(CustomUserForm):
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES)
    handed = forms.ChoiceField(choices=Student.HANDED_CHOICES)
    board = forms.ChoiceField(choices=Student.BOARD_CHOICES)
    stream = forms.ChoiceField(choices=Student.STREAM_CHOICES)
    grade = forms.ChoiceField(choices=Student.GRADE_CHOICES)
    admission_form_copy = forms.FileField(required=False)
    school_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_admission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    batch_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    father_name = forms.CharField(max_length=100)
    father_occupation = forms.CharField(max_length=100)
    mother_name = forms.CharField(max_length=100)
    mother_occupation = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

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
        ]



class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


from django import forms
from .models import Staff

class StaffForm(CustomUserForm):

    al_copy = forms.FileField(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    work_time_start = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}))
    work_time_end = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}))
    work_day_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) 
    work_day_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'designation',
                                               'mon_sal',
                                               'year_sal',
                                               'address',
                                               'subject_expertise',
                                               'entitled_el',
                                               'al_copy',
                                               'date_of_birth',
                                               'work_time_start',
                                               'work_time_end',
                                               'work_day_from',
                                               'work_day_to']

class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'designation',
                                               'mon_sal',
                                               'year_sal',
                                               'address',
                                               'subject_expertise',
                                               'entitled_el',
                                               'al_copy',
                                               'date_of_birth',
                                               'work_time_start',
                                               'work_time_end',
                                               'work_day_from',
                                               'work_day_to']



class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

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
            'mother_occupation',]


from django import forms
from .models import Staff

class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'designation',
                                               'mon_sal',
                                               'year_sal',
                                               'address',
                                               'subject_expertise',
                                               'entitled_el',
                                               'al_copy',
                                               'date_of_birth',
                                               'work_time_start',
                                               'work_time_end',
                                               'work_day_from',
                                               'work_day_to']

class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'designation',
                                               'mon_sal',
                                               'year_sal',
                                               'address',
                                               'subject_expertise',
                                               'entitled_el',
                                               'al_copy',
                                               'date_of_birth',
                                               'work_time_start',
                                               'work_time_end',
                                               'work_day_from',
                                               'work_day_to']


from django import forms
from .models import Event

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
        return cleaned_data

    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'shared_with_staff', 'select_all_staff', 'grade', 'board']

