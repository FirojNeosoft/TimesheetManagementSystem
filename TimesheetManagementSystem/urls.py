"""TimesheetManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from .views import LoginView, LogoutView, ChangePasswordView, CompanyView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='TMS APIs')

urlpatterns = [
    path('login/', LoginView.as_view(), name="sys_login"),
    path('logout/', LogoutView.as_view(), name="sys_logout"),
    path('', CompanyView.as_view(), name="company_choice"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('schema/', schema_view),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('tracker/', include('tracker.urls')),
    path('tracker/api/', include('tracker.rest_api.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

