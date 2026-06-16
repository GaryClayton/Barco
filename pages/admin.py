from django.contrib import admin
from .models import Page, ClubDefaults
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import resources


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'update_date')
    ordering = ('title',)
    search_fields = ('title',)


class ClubDefaultsAdmin(admin.ModelAdmin):
    list_display = ('club_id', 'club_name')
    ordering = ('club_id',)
    search_fields = ('club_id', 'club_name')


admin.site.register(Page, PageAdmin)
admin.site.register(ClubDefaults, ClubDefaultsAdmin)
