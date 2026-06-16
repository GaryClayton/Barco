from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddUserForm, EditUserForm
from pages.views import log_entry
from django.db.models.functions import Lower

def in_author_group(user):
    return user.is_authenticated and user.groups.filter(name="Author").exists()


@user_passes_test(in_author_group)
def user_list(request):
    hidden = getattr(settings, "EMAIL_EXCLUDE", [])
    users = (
        User.objects
        .exclude(username__in=hidden)
        .exclude(is_superuser=True)
        .order_by(Lower("username"))
    )
    return render(request, 'user_admin/staff/user_list.html', {'users': users})


@user_passes_test(in_author_group)
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            log_entry(request, "Add User - " + user.username, category='Add', importance='Low')
            return redirect('staff_user_list')
    else:
        form = AddUserForm()  # <-- MUST be blank

    return render(request, 'user_admin/staff/add_user.html', {'form': form})


@user_passes_test(in_author_group)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            log_entry(request, "Edit User - " + user.username, category='Edit', importance='Low')
            return redirect('staff_user_list')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'user_admin/staff/edit_user.html', {'form': form, 'user': user})


@user_passes_test(in_author_group)
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            log_entry(request, "Password Reset - " + user.username, category='Edit', importance='Low')
            return redirect('staff_user_list')
    else:
        form = SetPasswordForm(user)
    return render(request, 'user_admin/staff/reset_password.html', {
        'form': form,
        'user': user
    })


@user_passes_test(in_author_group)
def toggle_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('staff_user_list')
