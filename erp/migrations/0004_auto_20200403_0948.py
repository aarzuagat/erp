# Generated by Django 3.0.4 on 2020-04-03 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_auto_20200402_1827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyconfiguration',
            options={'ordering': ['shortName']},
        ),
        migrations.AlterField(
            model_name='company',
            name='isActive',
            field=models.IntegerField(default=1),
        ),
    ]
