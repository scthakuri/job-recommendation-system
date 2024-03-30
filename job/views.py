from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import View

from job.models import *
from job.utils import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import requests
import urllib.parse
from datetime import datetime, timedelta
import random
import re

from faker import Faker
fake = Faker()

IT_jobs = [
    {"title": "Software Developer", "skills": ["Python", "Java", "JavaScript", "SQL", "Git"]},
    {"title": "Data Scientist", "skills": ["Python", "R", "Machine Learning", "Statistics", "Data Visualization"]},
    {"title": "Web Developer", "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"]},
    {"title": "Network Engineer", "skills": ["Networking", "Cisco", "TCP/IP", "Firewalls", "Security"]},
    {"title": "Systems Administrator", "skills": ["Linux", "Windows Server", "Active Directory", "Shell Scripting"]},
    {"title": "IT Support Specialist", "skills": ["Troubleshooting", "Customer Service", "Hardware", "Software"]},
    {"title": "Cybersecurity Analyst", "skills": ["Cybersecurity", "Penetration Testing", "Incident Response", "SIEM", "Firewalls"]},
    {"title": "Cloud Engineer", "skills": ["AWS", "Azure", "Google Cloud Platform", "DevOps", "Infrastructure as Code"]},
    {"title": "Database Administrator", "skills": ["SQL", "MySQL", "Oracle", "Database Management", "Backup and Recovery"]},
    {"title": "UI/UX Designer", "skills": ["User Interface Design", "User Experience Design", "Prototyping", "Wireframing", "Adobe XD"]},
    {"title": "Machine Learning Engineer", "skills": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Neural Networks"]},
    {"title": "Quality Assurance Engineer", "skills": ["Quality Assurance", "Test Automation", "Selenium", "JUnit", "Bug Tracking"]},
    {"title": "DevOps Engineer", "skills": ["DevOps", "CI/CD", "Docker", "Kubernetes", "Ansible"]},
    {"title": "IT Project Manager", "skills": ["Project Management", "Agile Methodology", "Scrum", "Stakeholder Management", "Budgeting"]},
    {"title": "Systems Analyst", "skills": ["System Analysis", "Requirements Gathering", "UML", "Data Modeling", "Business Process Mapping"]},
    {"title": "App Developer", "skills": ["Mobile Development", "iOS", "Android", "Swift", "Java"]},
    {"title": "iOS Developer", "skills": ["iOS Development", "Swift", "Objective-C", "Xcode", "UIKit"]},
    {"title": "Frontend Developer", "skills": ["HTML", "CSS", "JavaScript", "React", "Angular"]},
    {"title": "Django Developer", "skills": ["Python", "Django", "RESTful API", "Database Management", "ORM"]},
    {"title": "Python Developer", "skills": ["Python", "Django", "Flask", "SQLAlchemy", "RESTful API"]},
    {"title": "PHP Developer", "skills": ["PHP", "MySQL", "Laravel", "Symfony", "CodeIgniter"]},
    {"title": "C++ Developer", "skills": ["C++", "Object-Oriented Programming", "Data Structures", "Algorithms", "STL"]},
    {"title": "C# Developer", "skills": ["C#", ".NET", "ASP.NET", "MVC", "Entity Framework"]},
    {"title": "Java Developer", "skills": ["Java", "Spring Framework", "Hibernate", "Maven", "JPA"]},
    {"title": "Ruby Developer", "skills": ["Ruby", "Ruby on Rails", "RSpec", "ActiveRecord", "RSpec"]},
    {"title": "Go Developer", "skills": ["Go", "Gorilla", "Gin", "Concurrency", "RESTful API"]},
]

job_descriptions = [
    "We are looking for a passionate {title} to join our team. The ideal candidate will have strong skills in {skills}.",
    "Join our dynamic team as a {title} and work on exciting projects using {skills}. Apply now!",
    "Are you a skilled {title} looking for new challenges? We want you! Apply today and showcase your expertise in {skills}.",
    "As a {title} at our company, you will be responsible for {skills}. Apply now and be part of our innovative team!",
]

# Create your views here.
class ScrapIndeedView(View):
    def get(self, request):
        companies = Company.objects.all()
        for _ in range(500):
            job_info = random.choice(IT_jobs)
            title = job_info["title"]
            
            company = random.choice(companies)
            skills_required = ', '.join(job_info["skills"])

            description_template = random.choice(job_descriptions)
            description = description_template.format(title=title, skills=skills_required)
            
            current_date = datetime.now()
            random_days = random.randint(0, 60)
            future_date = current_date + timedelta(days=random_days)
            expiry_date = future_date.strftime("%Y-%m-%d")
            
            job = Job.objects.create(
                title=title,
                description=description,
                company=company,
                skills_required=skills_required,
                salary=None,
                expiry_date=expiry_date,
            )
            print(f"Created job: {job.title} for company: {company.company_name}")

        return JsonResponse({
            "status": "success",
        })

class ScrapView(View):

    def remove_content_in_brackets(self, text):
        try:
            pattern = re.compile(r'\[.*?\]')
            cleaned_text = re.sub(pattern, '', text)
            return cleaned_text
        except Exception as e:
            pass
        return text

    def get_title(self, job_card):
        try:
            title = job_card.find_element(By.CSS_SELECTOR, '[itemprop="title"]').text
            return self.remove_content_in_brackets(title)
        except Exception as e:
            pass
        return None
    
    def get_company_name(self, job_card):
        try:
            return job_card.find_element(By.CSS_SELECTOR, 'h3[title]').text
        except Exception as e:
            pass
        return None
    
    def get_location(self, job_card):
        try:
            return job_card.find_element(By.CSS_SELECTOR, '.location [itemprop="addressLocality"]').text
        except Exception as e:
            pass
        return None
    
    def get_skills(self, job_card):
        skills = []
        try: 
            skill_tags = job_card.find_elements(By.CSS_SELECTOR, '[itemprop="skills"] .badge')
            for skill_tag in skill_tags:
                skills.append(skill_tag.text)

            return skills
        except Exception as e:
            pass
        title = self.get_title(job_card)
        if title:
            return title.split()
        return []
    
    def get_valid_through(self, job_card):
        try:
            jobtime = job_card.find_element(By.CSS_SELECTOR, '[itemprop="validThrough"]').get_attribute("content")
            if jobtime:
                date_obj = datetime.strptime(jobtime, "%B %d, %Y, %I:%M %p")
                return date_obj.strftime("%Y-%m-%d")
        except Exception as e:
            pass

        current_date = datetime.now()
        random_days = random.randint(0, 60)
        future_date = current_date + timedelta(days=random_days)
        return future_date.strftime("%Y-%m-%d")
    
    def get_image_src(self, job_card):
        try:
            return job_card.find_element(By.CSS_SELECTOR, '[itemprop="image"]').get_attribute("src")
        except Exception as e:
            pass
        return None
    
    def get_job_details(self, job_card):
        try:
            job_details = job_card.find_element(By.CSS_SELECTOR, '[itemprop="title"] a[title]')
            link = job_details.get_attribute("href")
            if link:
                pagedriver = webdriver.Chrome(options=self.chrome_options, service=self.service)
                pagedriver.get(link)
                description = pagedriver.find_element(By.CSS_SELECTOR, "#description").get_attribute('innerHTML')
                jobdes = pagedriver.find_element(By.CSS_SELECTOR, ".card-text[itemprop=description]").get_attribute('innerHTML')

                return (description, jobdes)
        except Exception as e:
            pass
        return None, None
    
    def get_latitude(self, location):
        try:
            url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(location) +'&format=json'
            response = requests.get(url).json()
            return (response[0]['lat'], response[0]['lon'])
        except Exception as e:
            pass
        return None, None

    def get(self, request, *args, **kwargs):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")

        self.service = Service()
        driver = webdriver.Chrome(options=self.chrome_options, service=self.service)
        for i in range(1, 7):
            print(f"Page: {i}")
            # driver.get(f"https://merojob.com/search/?q=&job_category=111&start_date=&end_date=&page={i}")
            # driver.get(f"https://merojob.com/category/it-telecommunication/?page={i}")
            driver.get(f"https://merojob.com/industry/software-companies/?page={i}")

            jobs = []
            try:
                job_cards = driver.find_elements(By.CSS_SELECTOR, '#search_job .card')
                for job_card in job_cards:
                    job_title = self.get_title(job_card)
                    if not job_title:
                        continue

                    company_name = self.get_company_name(job_card)
                    location = self.get_location(job_card)
                    lat, lng = self.get_latitude(location)

                    valid_through = self.get_valid_through(job_card)
                    image_src = self.get_image_src(job_card)
                    skills = self.get_skills(job_card)
                    cmpdes, jobdes = self.get_job_details(job_card)

                    try:
                        company = Company.objects.get(company_name=company_name)
                    except Company.DoesNotExist:
                        company = Company(
                            company_name = company_name,
                            description = cmpdes,
                            location = location,
                            logo = image_src,
                            lat = lat,
                            lng = lng
                        )
                        company.clean_fields()
                        company.save()
                    
                    job = Job(
                        title = job_title,
                        description = jobdes,
                        company = company,
                        skills_required = ', '.join(skills),
                        salary = None,
                        expiry_date = valid_through
                    )
                    job.clean_fields()
                    job.save()
                    
                    print(f"{job_title} Created Successfully")
            except Exception as e:
                pass

        return JsonResponse({
            "jobs": jobs
        })
    

class JobListView(View):
    def get(self, request, *args, **kwargs):
        jobs = recommend_jobs_with_skills_only("sql")
        print(jobs)

        return JsonResponse({
            "success": True
        })
    
class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        jobs = Job.objects.all()
        total_jobs = jobs.count()

        # if request.user.is_authenticated:
        #     jobs = recommend_jobs_with_skills_only(request.user.skills)

        lat = request.COOKIES.get('latitude') 
        lng = request.COOKIES.get('longitude')

        if request.user.is_authenticated and request.user.skills:
            if lat and lng:
                jobs = recommend_jobs_with_skills_and_location(request.user.skills, f"{lat},{lng}")
            else:
                jobs = recommend_jobs_with_skills_only(request.user.skills)
        else:
            if lat and lng:
                jobs = recommend_jobs_with_location_only(f"{lat},{lng}")
                
        return render(request, "front-page.html", context={
            "total_jobs" : total_jobs,
            "jobs" : jobs
        })
    
class SingleJobView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        job = get_object_or_404(Job, id=id)
        related_jobs = get_related_jobs(id)

        return render(request, "single-job.html", context={
            "job" : job,
            "related" : related_jobs
        })