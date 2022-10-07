from django import forms
from .models import *


class GetUrlForm(forms.Form):
    main_links = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form_for_ulr',
                                                                         'placeholder': "www.google.com",
                                                                         }))
