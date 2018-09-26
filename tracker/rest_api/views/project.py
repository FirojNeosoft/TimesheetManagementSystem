import logging, datetime

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from tracker.models import *
from tracker.utils import *
from tracker.rest_api.serializers.project import *


logger = logging.getLogger("tracker_log")


class ProjectActivitySet(viewsets.ModelViewSet):
    queryset = ProjectActivity.objects.all()
    serializer_class = ProjectActivitySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)
    permission_classes = (IsAuthenticated,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.exclude(status='Delete')
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)
    filter_fields = ('owner', 'status')
    permission_classes = (IsAuthenticated,)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.exclude(status='Delete')
    serializer_class = ContractSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('role', 'referral')
    ordering_fields = ('created_at',)
    filter_fields = ('employee', 'representative', 'client', 'billing_cycle', 'pay_rate_type', 'status')
    permission_classes = (IsAuthenticated,)


class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.exclude(status='Delete')
    serializer_class = TimesheetSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('contract',)
    ordering_fields = ('created_at',)
    filter_fields = ('contract', 'status')
    permission_classes = (IsAuthenticated,)


class TimesheetTaskViewSet(viewsets.ModelViewSet):
    queryset = TimesheetTask.objects.all()
    serializer_class = TimesheetTaskSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('note',)
    ordering_fields = ('created_at',)
    filter_fields = ('project', 'activity')
    permission_classes = (IsAuthenticated,)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.exclude(status='Delete')
    serializer_class = AssignmentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', 'description')
    ordering_fields = ('created_at', 'due_date')
    filter_fields = ('emp', 'status')
    permission_classes = (IsAuthenticated,)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.exclude(status='Delete')
    serializer_class = InvoiceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('remark',)
    ordering_fields = ('created_at',)
    filter_fields = ('client', 'status')
    permission_classes = (IsAuthenticated,)


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


class ReportView(APIView):
    # permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    def post(self, request, format=None):
        try:
            # import pdb; pdb.set_trace()
            from_date = datetime.strptime(request.data['from_date'], '%d/%m/%Y').date()
            to_date = datetime.strptime(request.data['to_date'], '%d/%m/%Y').date()
            list_contracts = get_report_data(request.data['resource_name'], from_date, to_date)
            print(list_contracts)
            return Response({
                'success': True,
                'message': 'Report generated.',
                'data': list_contracts
            })
        except Exception as e:
            logger.error("{}, error occured while generating report.".format(e))
            return Response({
                'success': False,
                'message': 'Something goes wrong while generating report.',
                'data': {}
            })
