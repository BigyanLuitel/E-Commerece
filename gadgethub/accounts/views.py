from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from .forms import SignUpForm, EmailLoginForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


class EmailLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailLoginForm