from django.forms import ModelForm
from django import forms
from .models import CRM, Company, CompanyContact, ClubContact
from events.models import Contribution


class CRMForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CRM
        fields = ['company', 'comment']


# ------------------ Edit Forms -------------------
class EditCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['id', 'name', 'sector', 'subsector', 'address', 'phone', 'email', 'web']


class EditCompanyContactForm(ModelForm):
    class Meta:
        model = CompanyContact
        fields = ['id', 'company', 'name', 'position', 'mobile', 'phone', 'email', 'emailconsent']


class EditClubContactForm(ModelForm):
    class Meta:
        model = ClubContact
        fields = ['id', 'company', 'name']


class EditCompanyContributionForm(ModelForm):
    class Meta:
        model = Contribution
        fields = ['id', 'company', 'support', 'value', 'event']


# ---------------------- Add Forms -------------------------------------
class AddNewCompanyForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = ['id', 'name', 'sector', 'subsector', 'address', 'phone', 'email', 'web']


class AddClubContactForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ClubContact
        fields = ['company', 'name']


class AddCompanyContactForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CompanyContact
        fields = ['company', 'name', 'position', 'mobile', 'phone', 'email','emailconsent']


class AddCompanyContributionForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Contribution
        fields = ['company', 'support', 'value', 'event']


class MultiFileImportForm(forms.Form):
    file1 = forms.FileField(label="TicketSource file - SalesReport.csv")
    file2 = forms.FileField(label="TicketSource file - QuestionnaireReport.csv")
    file3 = forms.FileField(label="Processed log file - Import tracking file (.csv)")
