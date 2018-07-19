import logging

from django.contrib.auth.models import User

from rest_framework import viewsets

from tracker.models import *
from tracker.rest_api.serializers.user import *


logger = logging.getLogger("tracker_log")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username', 'email')


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.exclude(status='Delete')
    serializer_class = EmployeeSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.exclude(status='Delete')
    serializer_class = ClientSerializer



