from django.contrib import admin
from .models import ClubMember, BusinessMeeting, Attendance, Guests
# Register your models here.


class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'username', 'dietary_requirements')


class BusinessMeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'meeting', 'attending')


class GuestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'meeting', 'sponsor', 'guest_name', 'guest_dr', 'comment')


admin.site.register(ClubMember, ClubMemberAdmin)
admin.site.register(BusinessMeeting, BusinessMeetingAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Guests, GuestsAdmin)
