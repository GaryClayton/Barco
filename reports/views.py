# System Imports
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

# Applications Imports
from barc_site.settings import EMAIL_BARCO, EMAIL_EXCLUDE, MEETING_CUTOFF_DAYS
from pages.models import Page, ClubDefaults
from pages.views import log_entry
from .models import ClubMember, Attendance, BusinessMeeting
from .utils.write_word import write_word_document
from .utils.write_excel import write_excel_document
from .utils.meetings import guests, members, meeting_date, meeting_report_email
from .forms import AddNewMeeting, ManageAttendance, MemberDiet, MeetingGuest
from .forms import EditClubDefaultForm
from companys.utils.user_session_data import UserState
from companys.models import CRM

# Start Views here


def user_is_in_group(request, group):
    if request.user.groups.filter(name=group).exists():
        return True
    else:
        return False


@login_required(login_url=reverse_lazy('login'))
def base_information(request):

    state = UserState(request)
    state.name = request.user.username
    state.user_id = request.user.id

    group_names = list(request.user.groups.values_list('name', flat=True))
    return render(request, 'reports/report_list.html', {'groups': group_names, 'Page_list': Page.objects.all()})


# Write the complete database to a file in documents type='Other'
@login_required(login_url=reverse_lazy('login'))
def write_excel(request):
    write_excel_document(request)  # separate file in utils
    log_entry(request, 'Excel file written', category='Archive', importance='Low')
    return render(request, 'reports/doc_success.html', {'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def write_word(request):
    write_word_document(request)  # separate file in utils
    log_entry(request, 'Word file written', category='Archive', importance='Low')
    return render(request, 'reports/doc_success.html', {'Page_list': Page.objects.all()})


# Compile the data for the full list of future meetings
@login_required(login_url=reverse_lazy('login'))
def meeting_log(request, typ):
    meetings = []

    # get list of meetings - GJC need to only list meeting in the future
    temp = BusinessMeeting.objects.all().order_by('date').filter(meeting_type=typ)
    temp2 = Attendance.objects.all().filter(member=request.user.id)
    temp3 = ClubMember.objects.all().filter(user_id=request.user.id)

    for meeting in temp:
        # Only add meetings to return if they are this or future months
        cutoff = datetime.date.today() - timedelta(days=MEETING_CUTOFF_DAYS)

        if meeting.date and meeting.date > cutoff:
            future = False
            if meeting.date > datetime.date.today() + timedelta(days=MEETING_CUTOFF_DAYS):
                future = True

            date = meeting.date.strftime("%b %d %Y")

            # Has the user said they are available or not in the past
            if meeting.meeting_type == 'Social':
                att = False  # social meetings are Opt-in
            elif meeting.meeting_type == 'Meeting':
                att = True  # business meetings are Opt-out
            else:
                print('meeting type error')  # A meeting should have been one of the above

            for attendance in temp2:
                if attendance.meeting.id == meeting.id:
                    if attendance.attending is False:
                        att = False
                    elif attendance.attending is True:
                        att = True

            # Compile meeting data

            mtg = [meeting.id, date, att, future, meeting.meeting_title, meeting.meeting_type]
            meetings.append(mtg)

    # Does the user have any dietary requirements
    dr = 'None'
    for diet_response in temp3:
        dr = diet_response.dietary_requirements

    data = [typ]

    return render(request, 'reports/meeting_manager.html',
                  {'meetings': meetings, 'diet': dr, 'data': data, 'Page_list': Page.objects.all()})


@login_required(login_url=reverse_lazy('login'))
def add_new_meeting(request):
    submitted = False
    if request.method == 'POST':
        form = AddNewMeeting(request.POST, request.FILES)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            return HttpResponseRedirect('/report/add_new_meeting?submitted=True')
    else:
        form = AddNewMeeting()
        if 'submitted' in request.GET:
            submitted = True

    log_entry(request, "New Meeting", category='Addition', importance='Low')

    return render(request, 'reports/add_new_meeting.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


@login_required(login_url=reverse_lazy('login'))
def manage_attendance(request, pk):
    submitted = False
    for mtg in BusinessMeeting.objects.filter(id=pk):
        typ = mtg.meeting_type
    if request.method == 'POST':
        form = ManageAttendance(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            if typ == 'Meeting':
                return HttpResponseRedirect('/report/meetings/Meeting')
            elif typ == 'Social':
                return HttpResponseRedirect('/report/meetings/Social')

    else:
        UserState(request).user_id = request.user.id
        form = ManageAttendance(initial={'member': request.user.id, 'meeting': pk})
        if 'submitted' in request.GET:
            submitted = True
        meeting = BusinessMeeting.objects.filter(id=pk)
        for mtg in meeting:
            details = [request.user.username, request.user.id,
                       mtg.id, mtg.meeting_title, mtg.location, mtg.date, mtg.meeting_time
                       ]

    return render(request, 'reports/manage_meeting_attendance.html',
                  {'form': form,
                   'Page_list': Page.objects.all(),
                   'submitted': submitted,
                   'details': details,
                   }
                  )


@login_required(login_url=reverse_lazy('login'))
def member_diet(request, typ):
    UserState(request).user_id = request.user.id
    UserState(request).name = request.user.username

    submitted = False
    if request.method == 'POST':
        form = MemberDiet(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            if typ == 'Meeting':
                return HttpResponseRedirect('/report/meetings/Meeting')
            elif typ == 'Social':
                return HttpResponseRedirect('/report/meetings/Social')
            else:
                return HttpResponseRedirect('/')
    else:
        UserState(request).user_id = request.user.id
        form = MemberDiet(initial={'user_id': request.user.id, 'username': request.user.username})
        if 'submitted' in request.GET:
            submitted = True

    log_entry(request, "Manage Member Dietary Requirements", category='Addition', importance='Low')

    return render(request, 'reports/member_dietary_requirements.html',
                  {'form': form,
                   'Page_list': Page.objects.all(),
                   'submitted': submitted
                   }
                  )


@login_required(login_url=reverse_lazy('login'))
def add_meeting_guest(request, pk):
    submitted = False
    typ = 'Meeting'  # set defaul return
    for mtg in BusinessMeeting.objects.filter(id=pk):
        typ = mtg.meeting_type
    if request.method == 'POST':
        form = MeetingGuest(request.POST, request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            if typ == 'Meeting':
                return HttpResponseRedirect('/report/meetings/Meeting')
            elif typ == 'Social':
                return HttpResponseRedirect('/report/meetings/Social')
            else:
                return HttpResponseRedirect('/')
    else:
        form = MeetingGuest(initial={'sponsor': request.user.id, 'meeting': pk})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'reports/add_meeting_guest.html',
                  {'form': form,
                   'Page_list': Page.objects.all(),
                   'submitted': submitted
                   }
                  )


@login_required(login_url=reverse_lazy('login'))
def meeting_report(request, pk):
    mtg = meeting_date(pk)
    ny, comming, nn, not_comming = members(pk)  # numbers-yes and numbers-no
    ng, guest = guests(pk)  # nembers-guests
    tm = ng + ny  # number-meals
    stats = [ny, nn, ng, tm]

    return render(request, 'reports/meeting_attendance_report.html',
                  {'id': pk,
                   'meeting': mtg,
                   'attending': comming,
                   'not_attending': not_comming,
                   'guests': guest,
                   'stats': stats,
                   'email': False,
                   'Page_list': Page.objects.all()
                   }
                  )


@login_required(login_url=reverse_lazy('login'))
def meeting_email(request, pk):
    email = request.user.email
    address = [email, EMAIL_BARCO]
    name = request.user.username
    subject = 'Business Meeting Attendance Report  -  ' + meeting_date(pk)
    message = name + ' has sent this report from Barco\n\n'

    message = message + meeting_report_email(request, pk)

    send_mail(subject, message, settings.EMAIL_HOST_USER, address)
    mtg = meeting_date(pk)
    ny, comming, nn, not_comming = members(pk)  # numbers-yes and numbers-no
    ng, guest = guests(pk)  # nembers-guests
    tm = ng + ny  # number-meals
    stats = [ny, nn, ng, tm]

    log_entry(request, "Meeting attendance email sent", category='Admin', importance='Low')
    return render(request, 'reports/meeting_attendance_report.html',
                  {'id': pk,
                   'meeting': mtg,
                   'attending': comming,
                   'not_attending': not_comming,
                   'guests': guest,
                   'stats': stats,
                   'email': True,
                   'Page_list': Page.objects.all()
                   }
                  )


@login_required(login_url=reverse_lazy('login'))
def edit_meeting(request, pk):
    typ = 'Meeting'
    for mtg in BusinessMeeting.objects.filter(id=pk):
        typ = mtg.meeting_type

    submitted = False
    mtg = get_object_or_404(BusinessMeeting, id=pk)
    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = AddNewMeeting(request.POST, instance=mtg)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()  # Save the updated book entry
            log_entry(request, "Edit Meeting " + str(pk), category='Edit', importance='Low')

            if typ == 'Meeting':
                return HttpResponseRedirect('/report/meetings/Meeting')
            elif typ == 'Social':
                return HttpResponseRedirect('/report/meetings/Social')
            else:
                return HttpResponseRedirect('/')
    else:
        # Pre-fill the form with the existing book data
        form = AddNewMeeting(instance=mtg)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'reports/add_new_meeting.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


def member_groups(request):
    members = (
        User.objects
        .exclude(username__in=EMAIL_EXCLUDE)
        .prefetch_related('groups')
        .order_by('username')
    )

    group_flags = {
        'Member': 'me',
        'CommunityService': 'cs',
        'Fundraising': 'fu',
        'MeetingManager': 'mm',
        'DocumentManager': 'dm',
        'Author': 'au',
    }

    data = []

    for member in members:
        flags = {key: False for key in group_flags.values()}

        for group in member.groups.all():
            for group_key, flag_key in group_flags.items():
                if group_key in group.name:
                    flags[flag_key] = True

        row = [member.username] + list(flags.values())
        data.append(row)

    return render(
        request,
        'reports/member_groups.html',
        {'data': data, 'Page_list': Page.objects.all()}
    )


@login_required(login_url=reverse_lazy('login'))
def edit_club_defaults(request):
    pk = 1968   # This is predetermined club id but should be the Author's own club only
    submitted = False
    mtg = get_object_or_404(ClubDefaults, club_id=pk)
    if request.method == 'POST':
        # Bind the form with POST data and the existing instance
        form = EditClubDefaultForm(request.POST, instance=mtg)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()  # Save the updated book entry
            log_entry(request, "Edit club defaults " + str(pk), category='Edit', importance='Low')

            return HttpResponseRedirect('/report/show')
    else:
        # Pre-fill the form with the existing book data
        form = EditClubDefaultForm(instance=mtg)
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'reports/edit_club_defaults.html',
                  {'form': form, 'Page_list': Page.objects.all(), 'submitted': submitted})


def crm_list(request):
    current_timespan = request.GET.get('timespan', 'all')  # Default to 'all'
    now = timezone.now()

    queryset = CRM.objects.all().order_by('-created')

    # Filter based on the dropdown selection
    if current_timespan == 'day':
        start_date = now - timedelta(days=1)
        queryset = queryset.filter(created__gte=start_date)
    elif current_timespan == 'week':
        start_date = now - timedelta(weeks=1)
        queryset = queryset.filter(created__gte=start_date)
    elif current_timespan == 'month':
        start_date = now - timedelta(days=30)
        queryset = queryset.filter(created__gte=start_date)

    context = {
        'crm_set': queryset,
        'current_timespan': current_timespan,
        'Page_list': Page.objects.all(),
    }
    return render(request, 'reports/crm_list.html', context)
