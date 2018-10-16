import datetime, decimal
import xhtml2pdf.pisa as pisa

from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import get_template

from tracker.models import *
from tenants.models import *

from io import BytesIO


class GetTenants(View):
    """
       Get contracts as role wise
    """

    def get(self, request):
        """
        Get contracts as role wise
        """
        company_list=[]
        companies = Company.objects.exclude(name='public')
        for company in companies:
            company_list.append({'name': company.name})
        return JsonResponse({'company_list': company_list})


class GetContracts(View):
    """
       Get contracts as role wise
    """

    def get(self, request):
        """
        Get contracts as role wise
        """

        if request.user.is_superuser:
            contracts = Contract.objects.exclude(status='Delete')
        elif not request.user.is_superuser and request.user.is_staff:
            contracts = (Contract.objects.filter(representative=request.user.employee) | Contract.objects.filter(employee=request.user.employee)).distinct()
        else:
            contracts = Contract.objects.filter(employee=request.user.employee)

        contract_list = []
        for contract in contracts:
            contract_list.append({'id': contract.id,
                                 'name': contract.__str__()})
        return JsonResponse({'contract_list': contract_list})


def get_report_data(name, from_date=datetime.today().date(), to_date=datetime.today().date()):
    """
      get report of an employee
    """
    first_name, last_name = name.split(' ')
    emp = Employee.objects.get(first_name=first_name.capitalize(), last_name=last_name.capitalize())
    contracts = Contract.objects.filter(employee=emp, created_at__range=[from_date, to_date]).exclude(status='Delete')
    list_contracts = []
    for contract in contracts:
        project_ids = Project.objects.filter(owner=contract.client).exclude(status='Delete').values_list('id',
                                                                                                         flat=False)
        timsheet_ids = Timesheet.objects.filter(contract=contract).exclude(status='Delete').values_list('id',
                                                                                                        flat=False)
        membership_details = ProjectMembership.objects.filter(employee=emp, project__in=project_ids)
        for member_detail in membership_details:
            project_tasks_from_timesheet = TimesheetTask.objects.filter(project=member_detail.project, \
                                                                        timesheet__in=timsheet_ids).aggregate(Sum('duration'))
            if project_tasks_from_timesheet['duration__sum']:
                actual_duration = round(decimal.Decimal(project_tasks_from_timesheet['duration__sum'].seconds / 3600),2)
            else:
                actual_duration = 0
            project_info = {
                "contract_name": contract.__str__(),
                'project_name': member_detail.project.name,
                'resource_cost': member_detail.cost,
                'planned_resource_duration': decimal.Decimal(member_detail.duration.seconds / 3600),
                'planned_total_cost': round(member_detail.cost * decimal.Decimal(member_detail.duration.seconds / 3600),2),
                'actual_resource_duration': actual_duration,
                'actual_total_cost': round(member_detail.cost * actual_duration,2)
                           }
            list_contracts.append(project_info)
        return list_contracts


class Render:

    @staticmethod
    def pdf_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


def get_defaulter(name, from_date=datetime.today().date(), to_date=datetime.today().date()):
    """
      get report of an employee
    """
    first_name, last_name = name.split(' ')
    emp = Employee.objects.get(first_name=first_name.capitalize(), last_name=last_name.capitalize())
    total_timesheet_count = abs((from_date - to_date).days)
    contracts = Contract.objects.filter(employee=emp, status='In progress')
    list_contracts = []
    for contract in contracts:
        submitted_timsheet_count = Timesheet.objects.filter(contract=contract, sign_in__range=[from_date, to_date]).count()
        remaining_timesheet_count = (total_timesheet_count - submitted_timsheet_count)
        if remaining_timesheet_count > 0:
            list_contracts.append({
                "resource_name": contract.employee.full_name,
                "client_name": contract.client.full_name,
                "remaining_timesheet_count": remaining_timesheet_count})
    return list_contracts
