from django import forms
from django.contrib.auth.models import User, Group


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            # Text-like inputs
            if widget.__class__.__name__ in ["TextInput", "EmailInput", "PasswordInput"]:
                # widget.attrs['class'] = 'form-control'
                widget.attrs['class'] = 'form-control form-control-sm'
            # Checkboxes
            elif widget.__class__.__name__ == "CheckboxInput":
                # widget.attrs['class'] = 'form-check-input'
                widget.attrs['class'] = 'form-check-input form-check-input-sm'

            # Checkbox groups (like Groups)
            elif widget.__class__.__name__ == "CheckboxSelectMultiple":
                widget.attrs['class'] = 'form-check-input'


class AddUserForm(BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # email_password = forms.BooleanField(required=False, label="Email password to user?")
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'groups']  # , 'email_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable browser autofill
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
        self.fields['password'].widget.attrs['autocomplete'] = 'new-password'


class EditUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'groups',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            # Text-like inputs
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({
                    'class': 'form-control',
                })

            # Checkboxes
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input',
                })

            # Groups (checkbox list)
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'form-check-input',
                })
