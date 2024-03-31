from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout, authenticate, login
from userauth.forms import LoginForm, RegisterForm
from django.views.generic import FormView
from django.urls import reverse_lazy

# Create your views here.
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("job:index")


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('job:index')
        else:
            return self.form_invalid(form)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(self.request, user)
            return redirect('job:index')
        else:
            return self.form_invalid(form)