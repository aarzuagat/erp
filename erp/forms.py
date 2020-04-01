from django import forms
from . import models

class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = '__all__'

class CompanyConfigurationForm(forms.ModelForm):
    class Meta:
        model = models.CompanyConfiguration
        fields = '__all__'