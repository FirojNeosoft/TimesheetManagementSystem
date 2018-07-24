from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate,login,logout


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        print(request.POST['username'], request.POST['password'])
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('login'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html')
