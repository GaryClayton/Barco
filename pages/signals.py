from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from pages.views import log_entry

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"Login Successful"
    log_entry(request, message, category='System', importance='Log Data')


@receiver(user_login_failed)
def log_user_login_failed(sender,  credentials, request, *args, **kwargs):
    username = credentials.get('username', 'Unknown')
    message = f"Login Failed - Unrecognised username= {username} or password"
    log_entry(request, message, category='System', importance='Log Data')


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    # Not used at this time to keep log records down to additions and edits
    message = f"User Logged Out"
    log_entry(request, message, category='System', importance='Log Data')

