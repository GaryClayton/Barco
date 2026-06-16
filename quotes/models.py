from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ('Minutes', 'Meeting Minutes'),
    ('Agenda', 'Meeting Agenda'),
    ('Council Minutes', 'Council Meeting Minutes'),
    ('Council Agenda', 'Council Meeting Agenda'),
    ('Accounts', 'Accounts'),
    ('CommitteeReports', 'Committee Reports'),
    ('Social', 'Scocial Events'),
    ('Car Show', 'Car Show Documents'),
    ('St Ed\'s Dinner', 'St Ed\'s Dinner Documents'),
    ('Golf Day', 'Golf Day Documents'),
    ('Auction', 'Auction Documents'),
    ('Press', 'Press Releases'),
    ('Logos', 'Company Logos'),
    ('Other', 'Other'),
    ('Training', 'Training & Manuals')
)

PRIORITY_CHOICES = (  # Not used
    ('U', 'Urgent - 1 week or less'),
    ('N', 'Normal - 2 to 4 weeks'),
    ('L', 'Low - Still Researching'),
)


class Quote(models.Model):
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Other')
    title = models.CharField(max_length=100)
    meetingdate = models.DateField(blank=False, null=False)
    submitted = models.DateField(auto_now_add=True)
    jobfile = models.FileField(upload_to='barc_root/uploads/', blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
