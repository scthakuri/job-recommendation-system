# Generated by Django 5.0.3 on 2024-03-21 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CompanyProfile',
            new_name='Company',
        ),
    ]
