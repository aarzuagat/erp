from django.db import models
from erp_crm import settings
from django.contrib.auth.models import User
class Company(models.Model):
    fiscalName = models.CharField(max_length=100)
    commercialName = models.CharField(max_length=100)
    nif = models.CharField(max_length=8)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    postalCode = models.CharField(max_length=20)
    isActive = models.IntegerField(default=1)

    class Meta:
        ordering = ['fiscalName']

    def __str__(self):
        return self.fiscalName
    
class CompanyConfiguration(models.Model):
    shortName = models.CharField(max_length=20)
    primaryColor = models.CharField(max_length=20)
    secondaryColor = models.CharField(max_length=20, null=True, blank=True)
    logo = models.ImageField(upload_to='companies/%Y/%m', null=True, blank=True)
    company = models.OneToOneField("Company", on_delete=models.CASCADE)

    class Meta:
        ordering = ['shortName']

    @property
    def logoUrl(self):
        if self.logo:
            return settings.SITE_URL+self.logo.url
        return None

class Emloyee(models.Model):
    name = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 100)
    email = models.EmailField()
    isActive = models.BooleanField(default=True)
    company = models.ForeignKey("Company", on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['lastName', 'name']

    def __str__(self):
        return f'{self.name} {self.lastName}'

class UserConfig(models.Model):
    viewMode = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
