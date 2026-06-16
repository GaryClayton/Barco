from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

from .models import Events, Contribution


class EventResource(resources.ModelResource):
    class Meta:
        model = Events


class ContributionResource(resources.ModelResource):
    class Meta:
        model = Contribution


class EventImportAdmin(ImportExportModelAdmin):
    resource_classes = [EventResource]
    list_display = ('id', 'name', 'year', 'date')


class ContributionImportAdmin(ImportExportModelAdmin):
    resource_classes = [ContributionResource]
    list_display = ('id', 'get_company', 'support', 'value', 'get_event')

    def get_company(self, obj):
        return obj.company.name

    def get_event(self, obj):
        return obj.event.name


admin.site.register(Events, EventImportAdmin)
admin.site.register(Contribution, ContributionImportAdmin)
