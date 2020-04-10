from django import forms
from . import models
from django.contrib.auth.models import Group, User

class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = '__all__'

class CompanyConfigurationForm(forms.ModelForm):
    class Meta:
        model = models.CompanyConfiguration
        fields = '__all__'

class RoleForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

