from django import forms
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import BookInstance

class CreateBookInstanceForm(forms.ModelForm):
    class Meta:
        model  = BookInstance
        fields = ['id','book','imprint','status','borrower','due_back']

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a data between now and 4 weeks (default 3).')
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        #Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more then 4 weeks ahead'))
        
        #Return cleaned data
        return data

