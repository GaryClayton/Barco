import datetime

from django.contrib.auth.models import User

from reports.models import ClubMember, Attendance, BusinessMeeting, Guests
from barc_site.settings import EMAIL_EXCLUDE


def meeting_date(pk: int) -> str:
    # date of meeting being reported on
    temp = BusinessMeeting.objects.all().filter(id=pk)
    mtg = ''
    for m in temp:
        mtg = m.date.strftime("%b %d %Y")

    return mtg


def members(pk: int):
    # non_members = ['GaryClayton.M', 'GaryClayton.F', 'GaryClayton.C', 'GaryClayton.A', 'Admin', 'SuperUser']
    potential = User.objects.exclude(username__in=EMAIL_EXCLUDE).order_by('last_name')
    temp2 = Attendance.objects.all().filter(meeting=pk)
    mtg_qs = BusinessMeeting.objects.all().filter(id=pk)

    for mtg_entry in mtg_qs:
        mtg = mtg_entry

    comming = []
    not_comming = []

    ny = 0
    nn = 0
    for usr in potential:
        if usr.username not in EMAIL_EXCLUDE and usr.is_active:
            dr = ''
            if mtg.meeting_type == 'Social':
                att = False  # social meetings are Opt-in
            elif mtg.meeting_type == 'Meeting':
                att = True  # business meetings are Opt-out
            else:
                print('meeting type error')  # A meeting should have been one of the above

            for a in temp2:  # step through attendance records to see latest record
                if a.member == usr.id:
                    if a.attending is True:
                        att = True
                    elif a.attending is False:
                        att = False

            temp4 = ClubMember.objects.all().filter(user_id=usr.id)

            for t in temp4:
                dr = t.dietary_requirements

            interim = [usr.username, att, dr, usr.first_name, usr.last_name]

            if att is True:
                comming.append(interim)
                ny = ny + 1
            else:
                not_comming.append(interim)
                nn = nn + 1

    return ny, comming, nn, not_comming


def guests(pk: int):
    potential = User.objects.all()
    temp3 = Guests.objects.all().filter(meeting=pk)
    guest = []
    ng = 0
    sponsor = ''
    for g in temp3:
        for u in potential:
            if g.sponsor == u.id:
                sponsor = u.username
        t = [g.guest_name, sponsor, g.guest_dr, g.comment]
        guest.append(t)
        ng = ng + 1

    return ng, guest


def meeting_report_email(request, pk):

    mtg = meeting_date(pk)
    ng, guest = guests(pk)
    ny, comming, nn, not_comming = members(pk)

    message = f'Meeting report for Business Meeting date :- {mtg} requested by user {request.user.username}\n\n'

    message = message + f'Number of Guests {ng},\nNumber of Members {ny},\nTotal Number of Meals Needed = {ng + ny}\n\n'

    message = message + f'Number of members attending is {ny} \n'
    message = message + "Information order is :- \nSurname,\tName   ,\tDietary Req's\n"
    if len(comming) > 0:
        max_surname = max(len(row[4]) for row in comming)
        max_first = max(len(row[3]) for row in comming)

        for temp in comming:
            message = message + (
                temp[4].ljust(max_surname + 2) + "\t" +
                temp[3].ljust(max_first + 2) + "\t" +
                temp[2] + '\n'
                 )

    message = message + '\n\n'
    message = message + f'Number of members not attending is {nn} \n'

    if len(not_comming) > 0:
        max_surname = max(len(row[4]) for row in not_comming)
        max_first = max(len(row[3]) for row in not_comming)

        for temp in not_comming:
            message = message + (
                    temp[4].ljust(max_surname + 2) + "\t" +
                    temp[3].ljust(max_first + 2) + "\t" +
                    temp[2] + '\n'
            )

    message = message + f'Number of quests attending is {ng} \n'
    if len(guest) > 0:
        message = message + "Information order is :- \nName, \tAdded by, \tDietary Req's, \tRepresenting\n"

    for temp in guest:
        message = message + f'{temp[0]}, \t{temp[1]}, \t{temp[2]}, \t{temp[3]}\n'
    message = message + '\n'

    return message
