from django.forms import ModelForm
# from companys.forms import LastKnownInformation
from .models import Events


class AddNewEventForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['company'].initial = LastKnownInformation.last_company_detail_viewed

    class Meta:
        model = Events
        fields = ['name', 'year', 'date']
