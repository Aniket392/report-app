from django import forms
from django.contrib import admin
from ajax_select.fields import autoselect_fields_check_can_add
from .models import Profile
from .forms import ProfileSearchForm

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]
    form = ProfileSearchForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        autoselect_fields_check_can_add(form, self.model, request.user)
        return form

admin.site.register(Profile, ProfileAdmin)