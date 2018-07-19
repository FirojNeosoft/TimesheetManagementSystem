import logging

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from tracker.models import *
from tracker.rest_api.serializers.project import *


logger = logging.getLogger("tracker_log")


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.exclude(status='Delete')
    serializer_class = ProjectSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.exclude(status='Delete')
    serializer_class = ContractSerializer


class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.exclude(status='Delete')
    serializer_class = TimesheetSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.exclude(status='Delete')
    serializer_class = InvoiceSerializer


class ListProjectsOfEmployee(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, emp_id, format=None):
        """
        Return a list of all projects.
        """
        emp = Employee.objects.get(id=emp_id)
        serializer = ContractSerializer(emp.contract.all(), many=True)
        return Response(serializer.data)


class ListEmployeesOfProject(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, project_id, format=None):
        """
        Return a list of all employees.
        """
        project = Project.objects.get(id=project_id)
        serializer = ContractSerializer(project.contract.all(), many=True)
        return Response(serializer.data)


class ListTimesheetsOfEmployee(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, emp_id, format=None):
        """
        Return a list of all timesheets.
        """
        data = []
        emp = Employee.objects.get(id=emp_id)
        for contract in emp.contract.all():
            serializer = TimesheetSerializer(contract.timesheet.all(), many=True)
            data.extend(serializer.data)
        return Response(data)


class ListTimesheetsOfProject(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, project_id, format=None):
        """
        Return a list of all timesheets.
        """
        data = []
        project = Project.objects.get(id=project_id)
        for contract in project.contract.all():
            serializer = TimesheetSerializer(contract.timesheet.all(), many=True)
            data.extend(serializer.data)
        return Response(data)
