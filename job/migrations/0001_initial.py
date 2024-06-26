# Generated by Django 5.0.3 on 2024-03-21 05:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('industry', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('location', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('skills_required', models.TextField()),
                ('salary', models.CharField(blank=True, max_length=100, null=True)),
                ('expiry_date', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UserInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_type', models.CharField(choices=[('VIEWED', 'Viewed'), ('APPLIED', 'Applied')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
