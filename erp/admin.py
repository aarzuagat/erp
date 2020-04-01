from django.contrib import admin
from . import models

admin.site.register(models.Company)
admin.site.register(models.CompanyConfiguration)

# Register your models here.
