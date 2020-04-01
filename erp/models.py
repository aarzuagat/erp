from django.db import models

class Company(models.Model):
    fiscalName = models.CharField(max_length=100)
    commercialName = models.CharField(max_length=100)
    nif = models.CharField(max_length=8)
    email = models.EmailField()
    website = models.URLField(null=True)
    telephone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    postalCode = models.CharField(max_length=20)
    configuration = models.OneToOneField("CompanyConfiguration", on_delete=models.CASCADE, null=True)

    
    def __str__(self):
        return self.fiscalName
    
class CompanyConfiguration(models.Model):
    shortName = models.CharField(max_length=20)
    primaryColor = models.CharField(max_length=20)
    secondaryColor = models.CharField(max_length=20, null=True)
    logo = models.ImageField(upload_to='companies/%Y/%m', null=True)

    def __str__(self):
        return self.shortName
