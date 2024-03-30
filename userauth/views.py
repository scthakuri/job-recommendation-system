from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout

# Create your views here.
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("job:index")