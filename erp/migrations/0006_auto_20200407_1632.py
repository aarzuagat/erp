# Generated by Django 3.0.4 on 2020-04-07 20:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0005_emloyee_userconfig'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Emloyee',
            new_name='Employee',
        ),
    ]