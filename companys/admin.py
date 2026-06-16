
from django.contrib import admin
from .models import Company, ClubContact, CompanyContact, CRM
from import_export.admin import ImportExportModelAdmin
from import_export import resources


# Previous non-import model
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sector', 'subsector', 'address', 'phone', 'email', 'web')
    list_filter = ('sector',)


class CompanyContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'name', 'position', 'phone', 'mobile', 'email')


class ClubContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'name')


class CRMAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'created', 'company', 'comment')


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyContact, CompanyContactAdmin)
admin.site.register(ClubContact, ClubContactAdmin)
admin.site.register(CRM, CRMAdmin)
