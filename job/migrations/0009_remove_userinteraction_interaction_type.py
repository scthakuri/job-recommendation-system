# Generated by Django 5.0.3 on 2024-03-30 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_alter_company_lat_alter_company_lng'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinteraction',
            name='interaction_type',
        ),
    ]
