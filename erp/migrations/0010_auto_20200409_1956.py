# Generated by Django 3.0.4 on 2020-04-09 23:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0009_remove_token_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='lastAccess',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='token',
            name='numberAccess',
            field=models.IntegerField(default=0),
        ),
    ]
