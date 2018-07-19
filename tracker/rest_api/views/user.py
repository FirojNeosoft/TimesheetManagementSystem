import logging

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters

from tracker.models import *
from tracker.rest_api.serializers.user import *


logger = logging.getLogger("tracker_log")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    filter_fields = ('username', 'email', 'is_staff')


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.exclude(status='Delete')
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'mobile', 'email', 'skype_id')
    ordering_fields = ('first_name', 'last_name', 'email', 'skype_id')
    filter_fields = ('gender', 'department', 'designation', 'employment_type', 'current_pay_rate_type',\
                  'current_visa_status', 'status')


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.exclude(status='Delete')
    serializer_class = ClientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'mobile', 'email', 'skype_id')
    ordering_fields = ('first_name', 'last_name', 'email', 'skype_id')
    filter_fields = ('gender', 'status')


