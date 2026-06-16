from django.core.management.base import BaseCommand
from pages.scheduled_tasks.email_tasks import send_meeting_reminder


class Command(BaseCommand):
    help = "Send meeting reminder 11 days before meeting date"

    def handle(self, *args, **kwargs):
        send_meeting_reminder()
        self.stdout.write(self.style.SUCCESS("Reminder check completed."))
