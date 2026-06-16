from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import time
import sys
from reports.models import BusinessMeeting
from pages.models import ClubDefaults
from datetime import datetime, timedelta


def send_barco_email(subject, message, bcc_list, html_message):
    max_retries = 5
    retry_delay = 300  # 5 minutes (in seconds)
    for attempt in range(1, max_retries + 1):
        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=message,  # Plain text version
                from_email=settings.EMAIL_HOST_USER,
                to=["bseabbey@gmail.com"],
                bcc=bcc_list,
            )
            msg.attach_alternative(html_message, "text/html")  # HTML version
            msg.send()
            print("✅ Meeting reminder sent.")
            break  # Success! Exit the loop.
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("All attempts failed. Exiting.")
                sys.exit(1)  # Exit with error code, so it shows as 'Failed' in logs


def send_meeting_reminder():
    today = timezone.localdate()

    bcc_list = []
    emails = User.objects.exclude(email="").values_list("email", flat=True).distinct()
    for address in emails:
        bcc_list.append(address)
    # bcc_list = ["gary.clayton.gc@googlemail.com"]  # Overwrites DB query for test purposes

    meetings = BusinessMeeting.objects.filter(date__gt=today)
    # meetings = BusinessMeeting.objects.filter(date__gte=today) # User for test purposes

    count = 0
    if not meetings.exists():
        print("ℹ No future meetings in database.")
    else:
        for meeting in meetings:
            date = meeting.date.strftime('%A %d %B %Y')
            start_dt = datetime.combine(meeting.date, meeting.meeting_time)
            # Subtract 30 minutes
            arrive_by_dt = start_dt - timedelta(minutes=30)
            arrive_by = arrive_by_dt.time()

            last_opp = meeting.date - timedelta(days=meeting.last_change_date)
            context = [date,
                       meeting.meeting_time,
                       arrive_by,
                       last_opp,
                       meeting.location,
                       meeting.organiser_name,
                       meeting.organiser_position,
                       meeting.organiser_telephone,
                       meeting.organiser_email,
                       meeting.meeting_title,
                       ]

            formatted_date = meeting.date.strftime('%A %d %B %Y')
            print(meeting.meeting_type,
                  meeting.meeting_title,
                  meeting.date - timedelta(days=meeting.first_email),
                  meeting.first_email)
            if meeting.meeting_type == 'Meeting' \
                    and meeting.date == today + timedelta(days=meeting.first_email) \
                    and meeting.first_email != 0:
                html_message = render_to_string('pages/emails/first_mtg_reminder.html', {'meeting': context})
                message = strip_tags(html_message)
                subject = f"Reminder: Business Meeting on {formatted_date}"
                send_barco_email(subject, message, bcc_list, html_message=html_message)
                count += 1
                print("✓ First Business meeting reminder sent today.")
            elif meeting.meeting_type == 'Meeting' \
                    and meeting.date == today + timedelta(days=meeting.second_email) \
                    and meeting.second_email != 0:
                html_message = render_to_string('pages/emails/second_mtg_reminder.html', {'meeting': context})
                message = strip_tags(html_message)
                subject = f"Reminder: Business Meeting on {formatted_date}"
                send_barco_email(subject, message, bcc_list, html_message=html_message)
                count += 1
                print("✓ Second Business meeting reminder sent today.")
            elif meeting.meeting_type == 'Social' \
                    and meeting.date == today + timedelta(days=meeting.first_email) \
                    and meeting.first_email != 0:
                html_message = render_to_string('pages/emails/first_social_mtg_reminder.html', {'meeting': context})
                message = strip_tags(html_message)
                subject = f"Reminder: Social Event on {formatted_date}"
                send_barco_email(subject, message, bcc_list, html_message=html_message)
                count += 1
                print("✓ First Social meeting reminder sent today.")
            elif meeting.meeting_type == 'Social' \
                    and meeting.date == today + timedelta(days=meeting.second_email) \
                    and meeting.second_email != 0:
                html_message = render_to_string('pages/emails/second_social_mtg_reminder.html', {'meeting': context})
                message = strip_tags(html_message)
                subject = f"Reminder: Social Event on {formatted_date}"
                send_barco_email(subject, message, bcc_list, html_message=html_message)
                count += 1
                print("✓ Second Social meeting reminder sent today.")
        print(f"✓ {count} emails sent today")