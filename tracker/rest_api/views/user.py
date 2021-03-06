import logging

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters

from tracker.models import *
from tracker.rest_api.permissions import *
from tracker.rest_api.serializers.user import *


logger = logging.getLogger("tracker_log")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    filter_fields = ('username', 'email', 'is_staff')
    permission_classes = (IsSuperAdmin,)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.exclude(status='Delete')
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'mobile', 'email', 'skype_id')
    ordering_fields = ('first_name', 'last_name', 'email', 'skype_id')
    filter_fields = ('gender', 'department', 'designation', 'employment_type', 'current_pay_rate_type',\
                     'current_visa_status', 'status', 'is_manager')
    permission_classes = (IsSuperAdmin,)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.exclude(status='Delete')
    serializer_class = ClientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'mobile', 'email', 'skype_id')
    ordering_fields = ('first_name', 'last_name', 'email', 'skype_id')
    filter_fields = ('gender', 'status')
    permission_classes = (IsSuperAdmin,)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.exclude(status='Delete')
    serializer_class = VendorSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('organization_name', 'contact_person_name', 'mobile', 'email',)
    ordering_fields = ('organization_name', 'contact_person_name', 'email',)
    filter_fields = ('status',)
    permission_classes = (IsSuperAdmin,)


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.exclude(status='Delete')
    serializer_class = ReferralSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'mobile', 'email',)
    ordering_fields = ('first_name', 'last_name', 'email',)
    filter_fields = ('status',)
    permission_classes = (IsSuperAdmin,)
