from django import forms
from .models import Profile
from ajax_select.fields import AutoCompleteSelectField
from ajax_select import make_ajax_field
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ("user",)


class ProfileSearchForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ()
    # user = make_ajax_field(Profile, 'user', 'userlookup', help_text=None)
    user = AutoCompleteSelectField('userlookup', required=True, help_text=None)