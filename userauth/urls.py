from django.urls import path
from userauth.views import *

app_name = "userauth"
urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
