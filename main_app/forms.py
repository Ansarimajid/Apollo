from django import forms
from .models import Note, StaffNote, CustomUser, Student, Admin, Staff , Event


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


class StudentForm(CustomUserForm):
    board = forms.ChoiceField(choices=Student.BOARD_CHOICES)
    stream = forms.ChoiceField(choices=Student.STREAM_CHOICES)
    grade = forms.ChoiceField(choices=Student.GRADE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'board', 'stream', 'grade']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'designation',
                                               'mon_sal', 'year_sal']


class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'board', 'stream', 'grade']


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['phone_no',
                                               'alternate_phone_no',
                                               'designation',
                                               'mon_sal', 'year_sal']


from django import forms
from django.forms import DateTimeInput
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'start_datetime', 'end_datetime')
        widgets = {
            'start_datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
