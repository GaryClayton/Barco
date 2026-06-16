from datetime import date
from django.forms import ModelForm
from.models import Charity, CharityContact, CharityDonation


# ---------------------- Add Forms -------------------------------------
class AddNewCharityForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Charity
        fields = ['id', 'name', 'sector', 'overview', 'web', 'address', 'phone', 'number']


class AddCharityContactForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CharityContact
        fields = ['charity', 'name', 'title', 'phone', 'mobile', 'email', 'comment']


class AddCharityDonationForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()

    class Meta:
        model = CharityDonation
        fields = ['charity', 'date', 'comment', 'value']


# ----------------------- Edit Forms --------------------
class EditCharityForm(ModelForm):
    class Meta:
        model = Charity
        fields = ['id', 'name', 'sector', 'overview', 'web', 'address', 'phone', 'number']


class EditCharityContactForm(ModelForm):
    class Meta:
        model = CharityContact
        fields = ['id', 'charity', 'name', 'title', 'phone', 'mobile', 'email', 'comment']


class EditCharityDonationForm(ModelForm):
    class Meta:
        model = CharityDonation
        fields = ['id', 'charity', 'date', 'comment', 'value']

