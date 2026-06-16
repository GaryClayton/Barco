from django.db import models
from django.utils.timezone import now
import datetime


class Page(models.Model):
    title = models.CharField(max_length=60)
    permalink = models.CharField(max_length=12, unique=True)
    update_date = models.DateTimeField('Last Updated')
    bodytext = models.TextField('Page Content', blank=True)

    def __str__(self):
        return self.title


class ClubDefaults(models.Model):
    club_id = models.IntegerField(default=0)
    club_name = models.CharField(max_length=100)
    club_link = models.URLField(null=True, blank=True)

    secretary_name = models.CharField(blank=True, max_length=100)
    secretary_telephone = models.CharField(blank=True, max_length=15)
    secretary_position = models.CharField(blank=True, max_length=100)
    secretary_email = models.EmailField(blank=True)

    meeting_location = models.CharField(blank=True, max_length=100)
    meeting_time = models.TimeField(default=datetime.time(18, 30))

    reminder_1_days = models.IntegerField(default=13)
    reminder_2_days = models.IntegerField(default=8)
    attendance_change_days = models.IntegerField(default=6)
