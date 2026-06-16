import datetime

from django import forms
from django.forms import ModelForm
from .models import Quote


class QuoteForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meetingdate'].initial = datetime.date.today()

    class Meta:
        model = Quote
        fields = [
            'type', 'title', 'meetingdate', 'jobfile'
        ]
