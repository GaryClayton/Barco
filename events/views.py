from django.shortcuts import render
from django.template.context_processors import request

# Create your views here.

from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import AddNewEventForm
from .models import Events, Contribution
from companys.models import Company
from pages.models import Page
from pages.views import log_entry
import csv


@login_required(login_url=reverse_lazy('login'))
def EventList(request):
    events_list = []
    for ev in Events.objects.all():
        temp = [ev.id, ev.name, ev.year, ev.date]
        events_list.append(temp)

    # log_entry(request, "Event List Viewed")

    return render(request, 'events/events_list.html', {'data': events_list, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def EventView(request, pk):
    context = []
    sponsor = []
    context_total = 0
    sponsor_total = 0
    for contribution in Contribution.objects.filter(event=str(pk)):
        temp = [contribution.id]
        for company in Company.objects.filter(id=contribution.company.id):
            temp.append(str(company.name))
        temp.append(contribution.support)
        temp.append(contribution.value)
        temp.append(str(contribution.event))
        temp.append(contribution.company)
        if "sponsor" in contribution.support.lower():
            sponsor_total += contribution.value
            sponsor.append(temp)
        else:
            context_total += contribution.value
            context.append(temp)
    ev = Events.objects.get(id=str(pk))
    company_support = [sponsor_total + context_total, sponsor_total, context_total]
    # log_entry(request, "Event Viewed - " + ev.name)

    return render(request, 'events/contribution_detail.html',
                  {'sponsor': sponsor,
                   'data': context,
                   'sponsor_total': company_support,
                   'event': ev.name,
                   'Page_list': Page.objects.all()}
                  )


@login_required(login_url=reverse_lazy('login'))
def new_event_entry(request):
    submitted = False
    if request.method == 'POST':
        form = AddNewEventForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            try:
                '''quote.username = request.user
                quote.company = LastKnownInformation.last_company_detail_viewed'''
            except Exception:
                pass
            quote.save()
            log_entry(request, "New Event - " + str(quote.name), category='Addition', importance='Low')
            return HttpResponseRedirect('/event/add-event?submitted=True')
    else:
        form = AddNewEventForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/new_event_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


# -------------------------------------------------------------------------------
# Code below not to be used - temporary code for development purposes
def output_csv():
    temp = Events.objects.all()
    data = []
    for c in temp:
        temp2 = [c.id, c.name, c.year, c.date]
        data.append(temp2)
        with open('events.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write each row of data to the CSV file
            for row in data:
                writer.writerow(row)
    print('Events data written')

    temp = Contribution.objects.all()
    data = []
    for d in temp:
        temp2 = [d.id, d.support, d.value, d.event, d.company]
        data.append(temp2)
        with open('contribution.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write each row of data to the CSV file
            for row in data:
                writer.writerow(row)
    print('Contribution data written')
