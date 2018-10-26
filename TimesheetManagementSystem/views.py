import logging

from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

logger = logging.getLogger('tracker_log')


class LoginView(View):
    """
    Login view
    """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            logger.error('wrong credentials for user {}'.format(request.POST['username']))
            messages.error(request, 'Please check credentials.')
            return HttpResponseRedirect('')


class LogoutView(LoginRequiredMixin, View):
    """
    Logout view
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('company_choice'))


class ChangePasswordView(LoginRequiredMixin, View):
    """
    Change Password
    """
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            logger.error('Failed to change password by user {}'.format(request.user.username))
            messages.error(request, 'Error occured while changing password, please enter a proper password.')
        return redirect('change_password')


class CompanyView(View):
    """
    List companies or tenants
    """
    def get(self, request):
        return render(request, 'company_selection.html')

    def post(self, request):
        if request.POST['company_choice'] == 'Select Company':
            return render(request, 'company_selection.html')
        else:
            return HttpResponseRedirect('http://'+request.POST['company_choice']+'.'+request.get_host()+'/login')
