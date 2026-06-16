from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.utils import timezone

from barc_site.settings import EMAIL_EXCLUDE
from .models import Company
from .models import CompanyContact
from .models import ClubContact
from .models import CRM
from .forms import CRMForm, AddNewCompanyForm, AddCompanyContactForm
from .forms import AddClubContactForm, AddCompanyContributionForm
from .forms import EditCompanyForm, EditCompanyContactForm, EditClubContactForm, EditCompanyContributionForm
from .utils.user_session_data import UserState
from events.models import Events, Contribution
from pages.models import Page
from quotes.models import Quote
from pages.views import log_entry
from reports.views import user_is_in_group

# imports for looking at ticket source files
import csv
from django.core.files.storage import default_storage
from django.http import HttpResponse
from .forms import MultiFileImportForm


@login_required(login_url=reverse_lazy('login'))
def CompanyList(request):
    # Set last company viewed to 0 indicating no specific company selected
    state = UserState(request)
    state.last_company_viewed = 0

    company = [[c.id, c.name, c.sector, c.subsector] for c in Company.objects.all()]
    company.sort(key=lambda tup: tup[1])

    # Collate the first leters in database companies for quick look-up
    letter = []
    for c in company:
        if c[1][0] not in letter and c[1][0].isalpha():
            letter.append(c[1][0])

    # collect unique event years as contributions must be attached to an event
    year = []
    for c in Events.objects.all():
        if c.year not in year:
            year.append(c.year)

    # log_entry(request, 'Company List')

    return render(request, 'companys/company_list.html',
                  {'data': company, 'year': year, 'letter': letter, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def CompanyView(request, pk):
    state = UserState(request)
    state.last_company_viewed = pk
    # print('CompanyView - state.last_company_viewed = ', pk)
    company = []
    club = []
    organization = []
    contribution = []
    relationship = []
    company_c = CompanyContact.objects.all().filter(company=pk)
    club_c = ClubContact.objects.all().filter(company=pk)
    cha = Company.objects.all().filter(id=pk)
    crm = CRM.objects.all().filter(company=pk)
    cont = Contribution.objects.all().filter(company=pk)

    for c in cha:  # only single return expected due to filtered request
        temp = [c.id, c.name, c.sector, c.subsector, c.address, c.phone, c.email, c.web]
        organization.append(temp)
        UserState(request).name = c.name

    for d in company_c:  # multiple entries expected
        temp = [d.id, d.name, d.position, d.mobile, d.phone, d.email, d.company, d.emailconsent]
        company.append(temp)

    for e in club_c:  # multiple entries expected
        temp = [e.id, e.name, e.company]
        club.append(temp)

    for f in cont:  # multiple entries expected
        temp = [f.id, f.support, f.value]
        ev = Events.objects.all().filter(id=str(f.event))
        for g in ev:
            temp.append(g.name)
            temp.append(g.date)
        contribution.append(temp)

    for g in crm:
        temp = [g.id, g.username, g.created, g.comment]
        relationship.append(temp)
        relationship.sort(reverse=True)

    # log_entry(request, "Company Viewed - " + organization[0][1])

    return render(request, 'companys/company_detail.html',
                  {'data_c': organization,
                   'data_d': company,
                   'data_e': club,
                   'data_f': contribution,
                   'data_g': relationship,
                   'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def CompanyYear(request, pk):
    # get all contributions for all the events within requested year
    # first get all events within the requested year
    events = []
    e = Events.objects.all().filter(year=pk)
    for i in e:
        # second get the contributions for those events
        con = Contribution.objects.all().filter(event=i.id)
        for y in con:
            # get the names of the companies that made the contributions
            com = Company.objects.all().filter(id=str(y.company))
            for z in com:
                # construct entry
                temp = [z.name, z.id, i.name, i.id, y.support, y.value]
                events.append(temp)
    events.sort(key=lambda tup: tup[0])

    # log_entry(request, "Company by Year " + str(pk))

    return render(request, 'companys/company_year.html', {'year': pk, 'cont': events, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def CompanyLetter(request, pk):
    # get all companies with a single starting letter
    comp_by_letters = []
    e = Company.objects.all()
    for i in e:
        if i.name[0] == pk:
            temp = [i.id, i.name, i.sector, i.subsector]
            comp_by_letters.append(temp)

    comp_by_letters.sort(key=lambda tup: tup[1])
    # log_entry(request, "Companies by Letter" + str(pk))
    return render(request, 'companys/company_letter.html', {'letter': pk, 'cont': comp_by_letters,
                                                            'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def new_crm_entry(request):
    submitted = False
    if request.method == 'POST':
        form = CRMForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            try:
                quote.username = request.user
                quote.company = Company.objects.get(pk=UserState(request).last_company_viewed)
            except Exception as e:
                log_entry(request,
                          "Exception raised " + str(e) + 'adding CRM for ' +
                          str(quote.company), category='System', importance='Medium'
                          )
                pass

            quote.save()
            log_entry(request, "New CRM Entry " + str(quote.company), category='CRM', importance='Low')
            return HttpResponseRedirect('/company/show/' + str(quote.company))
    else:
        state = UserState(request)
        form = CRMForm(initial={'company': state.last_company_viewed})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/crm_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def edit_company(request, pk):
    submitted = False
    cmp = get_object_or_404(Company, id=pk)

    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditCompanyForm(request.POST, instance=cmp)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()  # Save the updated book entry
            log_entry(request, "Company " + cmp.name, category='Edit', importance='Low')
            return HttpResponseRedirect('/company/show/' + str(pk))
    else:
        # Pre-fill the form with the existing book data
        form = EditCompanyForm(instance=cmp)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/edit_company.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def new_company_entry(request):
    submitted = False
    if request.method == 'POST':
        form = AddNewCompanyForm(request.POST, request.FILES)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            log_entry(request, "New Company", category='Addition', importance='Low')
            return HttpResponseRedirect('/company/add-company?submitted=True')
    else:
        form = AddNewCompanyForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/new_company_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def edit_company_contact(request, pk):
    submitted = False
    cmp = get_object_or_404(CompanyContact, id=pk)

    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditCompanyContactForm(request.POST, instance=cmp)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()  # Save the updated book entry
            log_entry(request, "Company contact " + cmp.name, category='Edit', importance='Low')

            return HttpResponseRedirect('/company/show/' + str(cmp.company))
    else:
        # Pre-fill the form with the existing book data
        form = EditCompanyContactForm(instance=cmp)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/edit_company.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def new_company_contact_entry(request):
    submitted = False
    if request.method == 'POST':
        form = AddCompanyContactForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            log_entry(request, "New Company Contact", category='Addition', importance='Low')
            try:
                quote.company = Company.objects.get(pk=UserState(request).last_company_viewed)
            except Exception as e:
                log_entry(request,
                          "Exception raised " + str(e) + 'adding company contact for ' +
                          str(quote.company), category='System', importance='Medium'
                          )
                pass
            quote.save()

            return HttpResponseRedirect('/company/show/' + str(quote.company))
    else:
        state=UserState(request)
        form = AddCompanyContactForm(initial={'company': state.last_company_viewed})
        if 'submitted' in request.GET:
            submitted = True



    return render(request, 'companys/new_company_contact_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def edit_club_contact(request, pk):
    submitted = False
    cmp = get_object_or_404(ClubContact, id=pk)

    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditClubContactForm(request.POST, instance=cmp)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            log_entry(request, "Club contact " + str(cmp.name) + " at " + str(cmp.company), category='Edit',
                      importance='Low')

            return HttpResponseRedirect('/company/show/' + str(cmp.company))
    else:
        # Pre-fill the form with the existing book data
        form = EditClubContactForm(instance=cmp)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/edit_company.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def new_club_contract_entry(request):
    submitted = False
    if request.method == 'POST':
        form = AddClubContactForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            try:
                state=UserState(request)
                quote.company = Company.objects.get(pk=state.last_company_viewed)
            except Exception as e:
                log_entry(request,
                          "Exception raised " + str(e) + 'adding club contact for ' +
                          str(quote.company), category='System', importance='Medium'
                          )
                pass

            quote.save()
            log_entry(request, "Club Contact Form", category='Addition', importance='Low')
            return HttpResponseRedirect('/company/show/' + str(quote.company))
    else:
        state = UserState(request)
        form = AddClubContactForm(initial={'company': state.last_company_viewed})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/new_club_contact_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def edit_company_contribution(request, pk):
    submitted = False
    cmp = get_object_or_404(Contribution, id=pk)

    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditCompanyContributionForm(request.POST, instance=cmp)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            log_entry(request, str(cmp.company) + " Contribution for " + str(cmp.event), category='Edit',
                      importance='Low')

            return HttpResponseRedirect('/company/show/' + str(cmp.company))
    else:
        # Pre-fill the form with the existing book data
        form = EditCompanyContributionForm(instance=cmp)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/edit_company.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def new_company_contribution(request):
    submitted = False
    if request.method == 'POST':
        form = AddCompanyContributionForm(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            try:
                quote.company = Company.objects.get(pk=UserState(request).last_company_viewed)
            except Exception as e:
                log_entry(request,
                          "Exception raised " + str(e) + 'adding company contribution for ' +
                          str(quote.company), category='System', importance='Medium'
                          )
                pass
            quote.save()
            log_entry(request, "New Company Contribution", category='Addition', importance='Low')
            return HttpResponseRedirect('/company/show/' + str(quote.company))
    else:
        # name =  LastKnownInformation.Name
        state = UserState(request)
        name = state.name
        last_company = state.last_company_viewed
        # print(name, last_company)
        form = AddCompanyContributionForm(initial={'company': last_company})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'companys/new_company_contribution_entry.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted, 'name': name})


@login_required(login_url=reverse_lazy('login'))
def stats(request):
    # GJC the 2 lines below are to test the import of two filenames for car show stall holder import.
    # form = import_multiple(request)
    # return render(request, "companys/import_multiple.html", {"form": form})
    if user_is_in_group(request, 'Author'):
        # log_entry(request, 'Statistics')
        a = []
        h = 0
        i = []
        staff_users = User.objects.filter(is_active=True)
        for user in staff_users:
            if user.last_login is not None and user.username not in EMAIL_EXCLUDE:
                ll = user.last_login
                temp = [user.username, ll.day, ll.strftime("%B"), ll.year, ll.strftime("%H:%M:%S"), ll]
                a.append(temp)
            else:
                if user.last_login is None and user.username not in EMAIL_EXCLUDE:
                    created = user.date_joined
                    temp = [user.username, created.day, created.strftime("%B"), created.year, created.strftime("%H:%M:%S"), created]
                    i.append(temp)

        a.sort(key=lambda tup: tup[5], reverse=True)
        i.sort(key=lambda tup: tup[0], reverse=False)
        b = len(Company.objects.all())
        c = len(CompanyContact.objects.all())
        d = len(ClubContact.objects.all())
        e = len(Contribution.objects.all())
        f = len(CRM.objects.all())
        g = len(Quote.objects.all())
        h = len(Session.objects.filter(expire_date__gte=timezone.now()))

        return render(request, 'companys/stats.html', {'logged_in': a,
                                                       'companies': b,
                                                       'comp_cons': c,
                                                       'club_cons': d,
                                                       'contribs': e,
                                                       'crm': f,
                                                       'docs': g,
                                                       'authenticated': h,
                                                       'never_logged_in': i,
                                                       'Page_list': Page.objects.all()
                                                       })


# See top of Stats for how the test called the function add to menue item in reports -
# Find limited access point for this unless I can make it fool-proof
# Perhaps just select input files, test which is which and check if they are correct
# then have hidden accummulation filename - system only - in log_data csv perhaps?
def import_multiple(request):
    if request.method == "POST":
        print('in POST')
        form = MultiFileImportForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES["file1"]
            file2 = request.FILES["file2"]
            log_file = request.FILES["file3"]

            # Store the log file
            log_path = default_storage.save(log_file.name, log_file)

            # Process file1
            decoded1 = file1.read().decode("utf-8").splitlines()
            reader1 = csv.DictReader(decoded1)

            # Process file2
            decoded2 = file2.read().decode("utf-8").splitlines()
            reader2 = csv.DictReader(decoded2)

            created = 0
            updated = 0

            # Example: process both files the same way
            for reader in (reader1, reader2):
                print('file1 = ', file1.name, 'file2 = ', file2.name)
                for row in reader:
                    print(f"Reference: {row['Reference']}, Total: {row['Total']}")
                    if file1.name == 'salesReport.csv':
                        row2 = row
                    '''email = row.get("Email")

                    supporter, exists = Company.objects.get_or_create(
                        email=email,
                        defaults={
                            "first_name": row.get("FirstName"),
                            "last_name": row.get("LastName"),
                        }
                    )

                    if exists:
                        created += 1
                    else:
                        supporter.first_name = row.get("FirstName")
                        supporter.last_name = row.get("LastName")
                        supporter.save()
                        updated += 1'''
            print(row2)
            for question, response in row2.items():
                print(question, response)
            return HttpResponse(
                f"Done. Created {created}, updated {updated}. Log saved to {log_path}"
            )
    form = MultiFileImportForm()  # ← FIXED
    return form


