from django.urls import path

from .views import write_excel, base_information, write_word
from .views import meeting_log, add_new_meeting, manage_attendance, member_diet, add_meeting_guest
from .views import meeting_report, meeting_email, member_groups, edit_meeting
from .views import edit_club_defaults
from .views import crm_list

urlpatterns = [
    path('show/', base_information, name='varoius-reports'),
    path('excel/', write_excel, name='output-to-excel'),
    path('word/', write_word, name='output-to-word'),
    path('meetings/<str:typ>', meeting_log, name='meetings'),
    path('add_new_meeting/', add_new_meeting, name='add-new-meeting'),
    path('manage_meeting_attendance/<int:pk>', manage_attendance, name='manage-meeting-attendance'),
    path('member_dietary_requirements/<str:typ>', member_diet, name='member-dietary-requirements'),
    path('add_meeting_guest/<int:pk>', add_meeting_guest, name='add-meeting-guest'),
    path('meeting_attendance_report/<int:pk>', meeting_report, name='meeting-attendance-report'),
    path('email_meeting_report/<int:pk>', meeting_email, name='email-meeting-report'),
    path('member_groups/', member_groups, name='menber-groups'),
    path('edit_meeting/<int:pk>', edit_meeting, name='edit-meeting'),
    path('crm_list/', crm_list, name='crm_list'),
    path('club-defaults/', edit_club_defaults, name='club-defaults'),
]
