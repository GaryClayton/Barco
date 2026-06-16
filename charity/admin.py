from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

from .models import Charity, CharityDonation, CharityContact


class CharityResource(resources.ModelResource):
    class Meta:
        model = Charity


class CharityContactResource(resources.ModelResource):
    class Meta:
        model = CharityContact


class CharityDonationResource(resources.ModelResource):
    class Meta:
        model = CharityDonation


class CharityImportAdmin(ImportExportModelAdmin):
    resource_classes = [CharityResource]
    list_display = ('id', 'name', 'overview', 'web', 'address', 'phone')
    search_fields = ('id', 'name', 'overview', 'web', 'address', 'phone')
    # search_help_text = 'search_fields'


class CharityContactImportAdmin(ImportExportModelAdmin):
    resource_classes = [CharityContactResource]
    list_display = ('id', 'name', 'title', 'get_name', 'phone', 'mobile', 'email', 'comment')

    def get_name(self, obj):
        return obj.charity.name


class CharityDonationImportAdmin(ImportExportModelAdmin):
    resource_classes = [CharityDonationResource]
    list_display = ('id', 'get_name', 'date', 'value', 'comment', 'get_name')

    def get_name(self, obj):
        return obj.charity.name


admin.site.register(Charity, CharityImportAdmin)
admin.site.register(CharityContact, CharityContactImportAdmin)
admin.site.register(CharityDonation, CharityDonationImportAdmin)
