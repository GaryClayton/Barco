from django.urls import path

from .views import EventList, EventView, new_event_entry

urlpatterns = [
    path('show', EventList, name='show-events'),
    path('showed/<int:pk>', EventView, name='show-contributions'),
    path('add-event/', new_event_entry, name='new-event-entry'),
]
