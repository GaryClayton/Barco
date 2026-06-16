from django.db import models
from django.contrib.auth.models import User
import datetime
from pages.models import ClubDefaults


def get_default_location():
    return ClubDefaults.objects.first().meeting_location


def get_default_meeting_time():
    return ClubDefaults.objects.first().meeting_time


def get_default_reminder_1():
    return ClubDefaults.objects.first().reminder_1_days


def get_default_reminder_2():
    return ClubDefaults.objects.first().reminder_2_days


def get_default_change_days():
    return ClubDefaults.objects.first().attendance_change_days


# --------------  Added to make social gatherings more flexible --------------
def get_default_organiser_name():
    return ClubDefaults.objects.first().secretary_name


def get_default_organiser_telephone():
    return ClubDefaults.objects.first().secretary_telephone


def get_default_organiser_position():
    return ClubDefaults.objects.first().secretary_position


def get_default_organiser_email():
    return ClubDefaults.objects.first().secretary_email


# Create your models here.
class ClubMember(models.Model):
    user_id = models.IntegerField(default=User)
    username = models.CharField(max_length=60, blank=True)
    dietary_requirements = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return str(self.id)


class BusinessMeeting(models.Model):
    SOCIAL = 'Social'
    MEETING = 'Meeting'
    MEETING_CHOICES = [
        (SOCIAL, 'Social Meeting'),
        (MEETING, 'Business Meeting'),
    ]
    date = models.DateField(auto_now=False)
    location = models.CharField(max_length=100, default=get_default_location())
    meeting_time = models.TimeField(default=get_default_meeting_time())
    meeting_type = models.CharField(max_length=10, choices=MEETING_CHOICES, default=MEETING)
    meeting_title = models.CharField(max_length=100, default='Business Meeting')
    first_email = models.IntegerField(default=get_default_reminder_1)
    second_email = models.IntegerField(default=get_default_reminder_2)
    last_change_date = models.IntegerField(default=get_default_change_days())
    organiser_name = models.CharField(blank=True, max_length=100, default=get_default_organiser_name)
    organiser_telephone = models.CharField(blank=True, max_length=15, default=get_default_organiser_telephone)
    organiser_position = models.CharField(blank=True, max_length=100, default=get_default_organiser_position)
    organiser_email = models.EmailField(blank=True, default=get_default_organiser_email)

    def __str__(self):
        return str(self.id)


class Attendance(models.Model):
    member = models.IntegerField(default=User)
    meeting = models.ForeignKey(BusinessMeeting,  on_delete=models.CASCADE)
    attending = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Guests(models.Model):
    meeting = models.ForeignKey(BusinessMeeting,  on_delete=models.CASCADE)
    sponsor = models.IntegerField(default=User)
    guest_name = models.CharField(max_length=60, blank=False)
    guest_dr = models.CharField(max_length=60, blank=True)
    comment = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return str(self.id)
