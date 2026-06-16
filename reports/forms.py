from django.forms import ModelForm
from django import forms
from .models import BusinessMeeting, Attendance, ClubMember, Guests
from pages.models import ClubDefaults


class AddNewMeeting(ModelForm):
    class Meta:
        model = BusinessMeeting
        fields = ['id',
                  'date',
                  'location',
                  'meeting_time',
                  'meeting_type',
                  'meeting_title',
                  'first_email',
                  'second_email',
                  'last_change_date',
                  'organiser_name',
                  'organiser_telephone',
                  'organiser_position',
                  'organiser_email'
                  ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class ManageAttendance(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Attendance
        fields = ['member', 'meeting', 'attending']
        widgets = {
            'member': forms.HiddenInput(),
            'meeting': forms.HiddenInput(),
        }


class MemberDiet(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ClubMember
        fields = ['id', 'user_id', 'username', 'dietary_requirements']


class MeetingGuest(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Guests
        fields = ['id', 'meeting', 'sponsor', 'guest_name', 'guest_dr', 'comment']


class EditClubDefaultForm(ModelForm):
    class Meta:
        model = ClubDefaults
        fields = ['id',
                  'club_id',
                  'club_name',
                  'club_link',
                  'secretary_name',
                  'secretary_telephone',
                  'secretary_position',
                  'secretary_email',
                  'meeting_location',
                  'meeting_time',
                  'reminder_1_days',
                  'reminder_2_days',
                  'attendance_change_days'
                  ]
        help_texts = {
            'club_id': 'Club Information',
            'secretary_name': 'Default Secretary Details',
            'meeting_location': 'Default Meeting Details',
            'reminder_1_days': 'Reminder Email Settings'
        }

        widgets = {
            'club_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Bury St Edmunds Rotary Club'
            }),
            'secretary_email': forms.EmailInput(attrs={
                'placeholder': 'secretary@example.com'
            }),
            'meeting_time': forms.TextInput(attrs={
                'placeholder': 'e.g. 18:30'
            }),
        }

