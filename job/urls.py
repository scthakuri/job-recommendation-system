from django.urls import path
from job.views import *

app_name = "job"
urlpatterns = [
    path("scrap/", ScrapView.as_view(), name="scrap"),
    path("scrap/indeed/", ScrapIndeedView.as_view(), name="indeed"),
    path("list/", JobListView.as_view(), name="list"),
    path("", FrontPageView.as_view(), name="index"),
    path("job/<id>/", SingleJobView.as_view(), name="single"),
    path("jobs/", JobsView.as_view(), name="jobs"),
]
