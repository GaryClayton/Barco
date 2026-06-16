from django.urls import path
from .views import CharityList, CharityView, CharityOverview, CharityYear  # , CharityContactView, CharityDonationView
from .views import new_charity_entry, new_charity_contact_entry, new_charity_donation
from .views import edit_charity, edit_charity_contact, edit_charity_donation

urlpatterns = [
    path('show/<int:pk>', CharityView, name='charity-detail'),
    # path('showcc/<int:pk>', CharityDonationView.as_view(), name='charity_donation'),
    # path('showdd/<int:pk>', CharityContactView.as_view(), name='charity-contact'),
    path('show', CharityList, name='show-charity'),
    path('charity_overview/<int:pk>', CharityOverview, name='charity-overview'),
    path('charity_year/<int:pk>', CharityYear, name='charity-year'),
    path('add-charity/', new_charity_entry, name='new-charity-entry'),
    path('add-charity-contact/', new_charity_contact_entry, name='new-charity-contact-entry'),
    path('add-charity-donation/', new_charity_donation, name='new-charity-donation-entry'),
    path('edit-charity/<int:pk>/', edit_charity, name='edit-charity'),
    path('edit-charity-contact/<int:pk>/', edit_charity_contact, name='edit-charity-contact'),
    path('edit-charity-donation/<int:pk>/', edit_charity_donation, name='edit-charity-donation'),
]
