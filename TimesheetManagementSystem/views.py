from django.views import View
from django.shortcuts import render
from registration.forms import UserForm
from registration.models import User
from django.utils import translation

class Login(View):
    """
      Create Login Form
    """
    def get(self,request):
        form=UserForm()
        translation.activate("hi")
        return render(request,'login.html',{})

    def post(self,request):
        try:
            print(">>>",request.POST)
            user=User.objects.get(name=request.POST['name'])
            if user and user.password == request.POST['pwd']:
                return render(request, 'home.html', {})
            else:
                return render(request, 'login.html', {'msg':'Invalid Authentication'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'msg': 'Invalid Authentication'})

        # return render(request,'login.html',{})


class Signup(View):
    """
      Create Login Form
    """
    def get(self,request):
        form=UserForm()
        translation.activate("hi")
        return render(request,'register.html',{'form':form})

    def post(self,request):
        form=UserForm(request.POST)
        if form.is_valid():
            user=User.objects.create(name=form.cleaned_data['name'],password=form.cleaned_data['password'])
            print("registration=",user)
        return render(request, 'login.html',\
               {'msg':'User registered successfully.'})