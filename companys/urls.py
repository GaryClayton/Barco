from django.urls import path
# from . import views
from .views import CompanyList, CompanyView, CompanyYear, CompanyLetter
from .views import new_company_contact_entry, new_crm_entry, new_company_entry
from .views import stats, new_company_contribution, new_club_contract_entry
from .views import edit_company, edit_company_contact, edit_club_contact, edit_company_contribution

urlpatterns = [
    path('show/<int:pk>', CompanyView, name='company-detail'),
    # path('showcc/<int:pk>', ClubContactView.as_view(), name='club-contact'),
    # path('showdd/<int:pk>', CompanyContactView.as_view(), name='company-contact'),
    path('show', CompanyList, name='show-companys'),
    path('company_year/<int:pk>', CompanyYear, name='company-year'),
    path('company_letter/<str:pk>', CompanyLetter, name='company-letter'),
    path('add-company/', new_company_entry, name='new-company-entry'),
    path('add-company-contact/', new_company_contact_entry, name='new-company-contact-entry'),
    path('add-company-contribution/', new_company_contribution, name='new-company-contribution-entry'),
    path('add-club-contact/', new_club_contract_entry, name='new-club-contact-entry'),
    path('edit-company/<int:pk>/', edit_company, name='edit-company'),
    path('edit-company/', edit_company, name='edit-scompany'),
    path('edit-company-contact/<int:pk>', edit_company_contact, name='edit-company-contact'),
    path('edit-club-contact/<int:pk>', edit_club_contact, name='edit-club-contact'),
    path('edit-company-contribution/<int:pk>', edit_company_contribution, name='edit-club-contact'),
    path('', new_crm_entry, name='new-crm-entry'),
    path('stats', stats, name='site-stats'),
]
