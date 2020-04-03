from django.db import models
from erp_crm import settings
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

    # def __str__(self):
    #     return self.c
