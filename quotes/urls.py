from django.urls import path

from . import views
from .views import QuoteList, QuoteType, QuoteDelete, delete_file# , QuoteView
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', views.quote_req, name='quote-request'),
    path('show', QuoteList, name='show-quotes'),
    path('quote_type/<pk>', QuoteType, name='quote-type'),
    path('quote_delete/<pk>', QuoteDelete, name='quote-delete'),
    path('delete_file/<pk>', delete_file, name='delete-file'),
]
