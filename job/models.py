from django.db import models
from userauth.models import User
from django.urls import reverse


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    location = models.TextField( blank=True, null=True)
    lat = models.DecimalField(decimal_places=20, max_digits=40, blank=True, null=True)
    lng = models.DecimalField(decimal_places=20, max_digits=40, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    logo = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name
    

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    skills_required = models.TextField(null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.DateField()

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse('job:single', args=[str(self.slug)])


class UserInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('VIEWED', 'Viewed'),
        ('APPLIED', 'Applied'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)