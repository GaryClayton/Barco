from django.contrib import admin
from .models import Quote
from import_export.admin import ImportExportModelAdmin


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'title', 'meetingdate', 'submitted', 'jobfile', 'username')
    readonly_fields = ('submitted',)

class DocumentImportAdmin(ImportExportModelAdmin):
    resource_classes = [Quote]
    list_display = ('id', 'type', 'title', 'meetingdate', 'submitted', 'jobfile', 'username')

admin.site.register(Quote, DocumentImportAdmin)


