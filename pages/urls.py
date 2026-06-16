from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, {'pagename': ''}, name='home'),
    path('privacy_policy', views.privacy_policy, name='privacy-policy'),
    path('contact', views.contact, name='contact'),
    path('<str:pagename>', views.index, name='index'),
]