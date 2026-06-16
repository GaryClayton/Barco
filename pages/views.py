from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path
from datetime import datetime
# from django.dispatch import receiver
import csv

from .models import Page
from .forms import ContactForm


def index(request, pagename):
    pagename = '/' + pagename
    pg = get_object_or_404(Page, permalink=pagename)
    context = {
        'title': pg.title,
        'content': pg.bodytext,
        'last_updated': pg.update_date,
        'Page_list': Page.objects.all(),
    }
    # log_entry(request, 'Home Page')
    return render(request, 'pages/page.html', context)


def contact(request):
    submitted = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            # con = get_connection('django.core.mail.backends.smtp.EmailBackend')
            address = [cd['email'], 'bseabbey@gmail.com']
            name = cd['yourname']
            subject = cd['subject']
            message = name + ' has sent a message from Barco' \
                             ' website \n\n' + cd['message']
            send_mail(subject, message, settings.EMAIL_HOST_USER, address)
            #    connection=con
            # )
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    # log_entry(request, 'Contact Page')

    return render(request, 'pages/contact.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


def log_entry(request, message, category='None', importance='Normal'):
    excluded_log_types = ['System', 'User']

    # if request.username != '':
    user = request.user.username
    if user == '':
        user = 'Unknown'

    # prepare data for csv log file
    dt = datetime.now()
    date = dt.strftime("%Y-%m-%d %H:%M:%S")

    data = [str(request.user.username), str(date), str(message), category, importance]

    cwd = Path.cwd()
    dir_path = Path(cwd / 'barc_root' / 'log-data' / 'csv')
    # Create directory (including parents if needed)
    try:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f'make directory failed - cause =  {e}')

    # Open or create log file and write date
    file_path = Path(dir_path / 'activity_log.csv')
    with open(file_path, 'a', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(data)


def privacy_policy(request):
    # log_entry(request, 'Privacy Page')
    # print('In Privacy Policy - in views.py')
    return render(request, 'pages/privacy.html', {'Page_list': Page.objects.all()})

