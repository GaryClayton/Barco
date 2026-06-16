from django.urls import path
from . import staff_views
urlpatterns = [
    path('staff/users/', staff_views.user_list, name='staff_user_list'),
    path('staff/users/add/', staff_views.add_user, name='staff_add_user'),
    path('staff/users/<int:user_id>/edit/', staff_views.edit_user, name='staff_edit_user'),
    path('staff/users/<int:user_id>/reset-password/', staff_views.reset_password, name='staff_reset_password'),
    path('staff/users/<int:user_id>/toggle-active/', staff_views.toggle_active, name='staff_toggle_active'),
]
