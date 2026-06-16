from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import Charity
from .models import CharityContact
from .models import CharityDonation
from .forms import AddNewCharityForm, AddCharityContactForm, AddCharityDonationForm
from .forms import EditCharityForm, EditCharityContactForm, EditCharityDonationForm
from companys.utils.user_session_data import UserState
from pages.models import Page
from pages.views import log_entry
import csv


@login_required(login_url=reverse_lazy('login'))
def CharityList(request):
    charity = []
    for c in Charity.objects.all():
        temp = [c.id, c.name, c.sector, c.address]
        charity.append(temp)
    charity.sort(key=lambda tup: tup[1])

    # collect unique event years as contributions must be attached to an event
    y = []
    for c in CharityDonation.objects.all():
        if str(c.date.year) not in y:
            y.append(str(c.date.year))
    y.sort(key=lambda x: x[0])  # GJC sort not working

    # log_entry(request, 'Charity List')

    return render(request, 'charity/charity_list.html', {'data': charity, 'years': y, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def CharityView(request, pk):
    state = UserState(request)
    state.last_charity_viewed = pk
    donation = []
    charity = []
    contact = []
    don = CharityDonation.objects.all().filter(charity=pk)
    cha = Charity.objects.all().filter(id=pk)
    poc = CharityContact.objects.all().filter(charity=pk)

    for c in cha:  # only single return expected due to filtered request
        temp = [c.id, c.name, c.sector, c.overview, c.web, c.address, c.phone, c.number]
        charity.append(temp)

    for d in don:  # multiple entries expected
        if d.date.month >= 7:
            year = d.date.year + 1
        else:
            year = d.date.year
        temp = [d.id, year, d.value, d.comment, d.charity]
        donation.append(temp)

    for e in poc:  # multiple entries expected
        temp = [e.id, e.name, e.title, e.phone, e.mobile, e.email, e.comment]
        contact.append(temp)

    # log_entry(request, "Charity Viewed - " + charity[0][1])

    return render(request, 'charity/charity_detail.html', {'data_d': donation, 'data_c': charity, 'data_e': contact, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def CharityOverview(request, pk):
    cha = Charity.objects.all().filter(id=pk)
    temp = []
    for c in cha:  # only single return expected due to filtered request
        temp.append(c.overview)
        name = c.name

    # log_entry(request, "Charity Overview Viewed - " + name)

    return render(request, 'charity/charity_overview.html', {'data_c': temp, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def CharityYear(request, pk):
    # Need to compile data for charity donations in selected year
    chd = CharityDonation.objects.all()
    don = []
    for c in chd:
        if str(c.date.year) == str(pk):
            ref = str(c.charity.id)
            ch = Charity.objects.all().filter(id=str(c.charity))
            for z in ch:
                if str(z.id) == ref:
                    temp = [z.name, str(c.date), c.value, c.comment, ref]
                    don.append(temp)
    don.sort(key=lambda x: x[0])

    # log_entry(request, "Charity supported in year - " + str(pk))

    return render(request, 'charity/charity_year.html', {'year': pk, 'donation': don, 'Page_list': Page.objects.all()})


# -------------------- Add Entries ------------------------------
@login_required(login_url=reverse_lazy('login'))
def new_charity_entry(request):
    submitted = False
    if request.method == 'POST':
        form = AddNewCharityForm(request.POST, request.FILES)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            log_entry(request, "New Charity - " + str(quote.name), category='Addition', importance='Low')
            return HttpResponseRedirect('/charity/add-charity?submitted=True')
    else:
        form = AddNewCharityForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'charity/new_charity_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def new_charity_contact_entry(request):
    submitted = False
    if request.method == 'POST':
        form = AddCharityContactForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            try:
                state = UserState(request)
                quote.charity = state.last_charity_viewed
            except Exception:
                pass
            quote.save()
            log_entry(request, "New Charity Contact", category='Addition', importance='Low')
            return HttpResponseRedirect('/charity/show/' + str(quote.charity))
    else:
        state = UserState(request)
        print(state.last_charity_viewed)
        form = AddCharityContactForm(initial={'charity': state.last_charity_viewed})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'charity/new_charity_contact_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def new_charity_donation(request):
    submitted = False
    if request.method == 'POST':
        form = AddCharityDonationForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            try:
                quote.charity = UserState(request).last_charity_viewed
            except Exception:
                pass
            quote.save()
            log_entry(request, "New Charity Donation", category='Addition', importance='Low')
            return HttpResponseRedirect('/charity/show/' + str(quote.charity))
    else:
        state=UserState(request)
        form = AddCharityDonationForm(initial={'charity': state.last_charity_viewed})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'charity/new_charity_donation_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


# -----------------Edit Entries
@login_required(login_url=reverse_lazy('login'))
def edit_charity(request, pk):
    submitted = False
    cmp = get_object_or_404(Charity, id=pk)

    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditCharityForm(request.POST, instance=cmp)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()  # Save the updated book entry
            log_entry(request, "Charity " + cmp.name, category='Edit', importance='Low')
            return HttpResponseRedirect('/charity/show/' + str(cmp.id))
    else:
        # Pre-fill the form with the existing book data
        form = EditCharityForm(instance=cmp)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'charity/edit_charity.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def edit_charity_contact(request, pk):
    submitted = False
    cmp = get_object_or_404(CharityContact, id=pk)

    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditCharityContactForm(request.POST, instance=cmp)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()  # Save the updated book entry
            log_entry(request, "Charity Contact - " + str(quote.id) + ' ' + str(quote.name), category='Edit', importance='Low')
            return HttpResponseRedirect('/charity/show/' + str(cmp.charity))
    else:
        # Pre-fill the form with the existing book data
        form = EditCharityContactForm(instance=cmp)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'charity/edit_charity.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def edit_charity_donation(request, pk):
    submitted = False
    cmp = get_object_or_404(CharityDonation, id=pk)

    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditCharityDonationForm(request.POST, instance=cmp)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()  # Save the updated book entry
            log_entry(request, "Charity Donation - " + str(quote.id), category='Edit', importance='Low')
            return HttpResponseRedirect('/charity/show/' + str(cmp.charity))
    else:
        # Pre-fill the form with the existing book data
        form = EditCharityDonationForm(instance=cmp)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'charity/edit_charity.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


# ============================================================================
# Code below this line only used for development
# Do NOT NOT NOT run
#
def output_csv():
    temp = Charity.objects.all()
    data = []
    for c in temp:
        temp2 = [c.id, c.name, c.sector, c.overview, c.web, c.address, c.phone]
        data.append(temp2)
        with open('charity.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write each row of data to the CSV file
            for row in data:
                writer.writerow(row)
    print('Charity data written')

    temp = CharityContact.objects.all()
    data = []
    for e in temp:
        temp2 = [e.id, e.name, e.title, e.phone, e.mobile, e.email, e.comment]
        print(temp2)
        data.append(temp2)
        with open('charitycontact.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write each row of data to the CSV file
            for row in data:
                writer.writerow(row)
    print('Charity Contact data written')

    temp = CharityDonation.objects.all()
    data = []
    for d in temp:
        temp2 = [d.id, d.date, d.value, d.comment, d.charity]
        data.append(temp2)
        with open('charitydonation.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write each row of data to the CSV file
            for row in data:
                writer.writerow(row)
    print('Charity Donation data written')

