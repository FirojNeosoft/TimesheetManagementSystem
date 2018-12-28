import logging

from datetime import datetime

from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from tracker.models import *
from tracker.forms import *
from tracker.utils import *

from django.db import connection
from tenant_schemas.utils import (get_tenant_model, remove_www,get_public_schema_name)

logger = logging.getLogger('tracker_log')


class DashboardView(LoginRequiredMixin, View):
    """
    Dashboard
    """
    def get(self, request):
        """
          dashboard
        """
        form = DurationSearchForm()
        # import pdb; pdb.set_trace()
        # TenantModel = get_tenant_model()
        # t = TenantModel.objects.get(name='triveni')
        # request.tenant = t
        # connection.set_tenant(request.tenant)
        data = { "employees_count" : Employee.objects.exclude(status='Delete').count(),
        "clients_count" : Client.objects.exclude(status='Delete').count(),
        "projects_count" : Project.objects.exclude(status='Delete').count(),
        "contracts_count" : Contract.objects.exclude(status='Delete').count(),
                 "form":form}
        return render(request, 'dashboard.html', data)

    def post(self, request):
        try:
            form = DurationSearchForm(request.POST)
            data = {"employees_count": Employee.objects.exclude(status='Delete').count(),
                    "clients_count": Client.objects.exclude(status='Delete').count(),
                    "projects_count": Project.objects.exclude(status='Delete').count(),
                    "contracts_count": Contract.objects.exclude(status='Delete').count(),
                    "form": form}

            if form.is_valid():
                timesheet_result = {}
                timesheet_result['total_submitted_timesheet'] = Timesheet.objects.filter(sign_in__range=[form.cleaned_data['from_date'] , form.cleaned_data['to_date'] ]).\
                    exclude(contract__status='Delete').count()
                timesheet_result['total_pending_timesheet'] = Timesheet.objects.filter(sign_in__range=[form.cleaned_data['from_date'] , form.cleaned_data['to_date'] ], status='Pending').\
                    exclude(contract__status='Delete').count()
                timesheet_result['total_approved_timesheet'] = Timesheet.objects.filter(sign_in__range=[form.cleaned_data['from_date'] , form.cleaned_data['to_date'] ], status='Approved').\
                    exclude(contract__status='Delete').count()
                timesheet_result['total_rejected_timesheet'] = Timesheet.objects.filter(sign_in__range=[form.cleaned_data['from_date'] , form.cleaned_data['to_date'] ], status='Rejected').\
                    exclude(contract__status='Delete').count()
                data['timesheet_result'] = timesheet_result
                return render(request, 'dashboard.html', data)
            else:
                return render(request, 'dashboard.html', data)
        except Exception as e:
            logger.error("{}, error occured while searching timesheet data on dashboard.".format(e))
            messages.error(request, "Error occured while searching timesheet data on dashboard.")
            return redirect('dashboard')


class ListClientsView(LoginRequiredMixin, ListView):
    """
    List Clients
    """
    model = Client
    queryset = Client.objects.exclude(status='Delete')
    template_name = 'client_list.html'


class CreateClientView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new client
    """
    model = Client
    fields = ['first_name', 'last_name', 'gender', 'mobile', 'email', 'skype_id', 'document', 'status']
    template_name = 'client_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_clients')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            client = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            if city and country and state and zip_code:
                try:
                    client.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state,\
                                                            country=country,zip_code=int(zip_code))
                    client.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of a client.".format(e))
                    messages.error(request, "Error occured while saving address of a client.")
                    return redirect('add_client')
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_client')
        return HttpResponseRedirect(reverse('list_clients'))


class UpdateClientView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing client
    """
    model = Client
    fields = ['first_name', 'last_name', 'gender', 'mobile', 'email', 'skype_id', 'document', 'status']
    template_name = 'edit_client_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_clients')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Client.objects.get(id=pk)
        if obj.document:
            file_url = request.build_absolute_uri('/')[:-1]+obj.document.url
        else:
            file_url=''
        return render(request, 'edit_client_form.html', {'obj': obj, 'file_url':file_url})

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Client.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            client = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']

            if city and country and state and zip_code:
                try:
                    if client.address:
                        client.address.line1=line1
                        client.address.line2=line2
                        client.address.city_or_village=city
                        client.address.state=state
                        client.address.country=country
                        client.address.zip_code=int(zip_code)
                        client.address.save()
                    else:
                        client.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city,
                                                                state=state, country=country, zip_code=int(zip_code))
                        client.save()

                except Exception as e:
                    logger.error("{}, error occured while saving address of a client.".format(e))
                    messages.error(request, "Error occured while saving address of a client.")
                    return redirect('update_client', pk)
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_client', pk)
        return HttpResponseRedirect(reverse('list_clients'))


class DeleteClientView(LoginRequiredMixin, DeleteView):
    """
    Delete existing client
    """
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('list_clients')


class ListUsersView(LoginRequiredMixin, ListView):
    """
    List Users
    """
    model = User
    queryset = User.objects.all()
    template_name = 'user_list.html'


class CreateUserView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was created successfully"
    success_url = reverse_lazy('list_users')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password'])
            user.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_user')
        return HttpResponseRedirect(reverse('list_users'))


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was updated successfully"
    success_url = reverse_lazy('list_users')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('list_users')


class ListEmployeesView(LoginRequiredMixin, ListView):
    """
    List Employees
    """
    model = Employee
    queryset = Employee.objects.exclude(status='Delete')
    template_name = 'employees_list.html'


class CreateEmployeeView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new employee
    """
    model = Employee
    fields = ['first_name', 'last_name', 'employee_id', 'birth_date', 'gender', 'joined_date', 'mobile', 'email',\
              'skype_id', 'is_manager', 'department', 'designation', 'skills', 'employment_type','current_pay_rate_type',\
              'current_pay_rate', 'passport_no','current_visa_status', 'status', 'note']
    template_name = 'employee_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_employees')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            emp = form.save()

            if request.POST['location'] and request.POST['country'] and request.POST['state'] and request.POST['zip']:
                try:
                    emp.address = Address.objects.create(line1=request.POST['line1'], line2=request.POST['line2'],\
                                                         city_or_village=request.POST['location'], state=request.POST['state'],\
                                                         country=request.POST['country'],zip_code=int(request.POST['zip']))
                    emp.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of an employee.".format(e))
                    messages.error(request, "Error occured while saving address of an employee.")
                    return redirect('add_employee')

            if request.POST['relative_first_name'] and request.POST['relative_last_name'] and \
                                                             request.POST['relative_mobile'] and request.POST['relation']:
                try:
                    emp.emergency_contact = EmergencyContact.objects.create(first_name=request.POST['relative_first_name'], \
                                                                     last_name=request.POST['relative_last_name'], \
                                                    relation=request.POST['relation'], mobile=request.POST['mobile'],)
                    emp.save()
                except Exception as e:
                    logger.error("{}, error occured while saving emergency contact of an employee.".format(e))
                    messages.error(request, "Error occured while saving emergency contact of an employee.")
                    return redirect('add_employee')

            if request.POST['bank_name'] and request.POST['bank_routing_no'] and \
                                                request.POST['account_no'] and request.POST['account_type']:
                try:
                    emp.bank_account_info = BankAccountInfo.objects.create(bank_name=request.POST['bank_name'], \
                                                                           bank_routing_no=request.POST['bank_routing_no'], \
                                                    account_no=request.POST['account_no'], account_type=request.POST['account_type'],)
                    emp.save()
                except Exception as e:
                    logger.error("{}, error occured while saving bank information of an employee.".format(e))
                    messages.error(request, "Error occured while saving bank information of an employee.")
                    return redirect('add_employee')

            if request.POST['filling_status'] and request.POST['withholding_allowance']:
                try:
                    emp.tax_info = TaxInfo.objects.create(filling_status=request.POST['filling_status'], \
                                                            withholding_allowance=request.POST['withholding_allowance'], \
                                                            additional_withholding=request.POST['additional_withholding'],\
                                                            is_withholding_declare='is_withholding_declare' in request.POST)
                    emp.save()
                except Exception as e:
                    logger.error("{}, error occured while saving tax information of an employee.".format(e))
                    messages.error(request, "Error occured while saving tax information of an employee.")
                    return redirect('add_employee')

        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_employee')
        return HttpResponseRedirect(reverse('list_employees'))


class UpdateEmployeeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing employee
    """
    model = Employee
    fields = ['first_name', 'last_name', 'employee_id', 'birth_date', 'gender', 'joined_date', 'mobile', 'email',\
              'skype_id', 'is_manager', 'department', 'designation', 'skills', 'employment_type','current_pay_rate_type',\
              'current_pay_rate', 'passport_no','current_visa_status', 'status', 'note']
    template_name = 'edit_employee_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_employees')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Employee.objects.get(id=pk)
        return render(request, 'edit_employee_form.html', {'obj': obj})

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Employee.objects.get(id=pk)
        form = self.get_form()

        if form.is_valid():
            emp = form.save()

            if request.POST['location'] and request.POST['country'] and request.POST['state'] and request.POST['zip']:
                try:
                    if emp.address:
                        emp.address.line1= request.POST['line1']
                        emp.address.line2= request.POST['line2']
                        emp.address.city_or_village= request.POST['location']
                        emp.address.state= request.POST['state']
                        emp.address.country= request.POST['country']
                        emp.address.zip_code= int(request.POST['zip'])
                        emp.address.save()
                    else:
                        emp.address = Address.objects.create(line1=request.POST['line1'], line2=request.POST['line2'], \
                                                             city_or_village=request.POST['location'],
                                                             state=request.POST['state'], \
                                                             country=request.POST['country'],
                                                             zip_code=int(request.POST['zip']))
                        emp.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of an employee.".format(e))
                    messages.error(request, "Error occured while saving address of an employee.")
                    return redirect('update_employee', pk)

            if request.POST['relative_first_name'] and request.POST['relative_last_name'] and \
                                                             request.POST['relative_mobile'] and request.POST['relation']:
                try:
                    if emp.emergency_contact:
                        emp.emergency_contact.first_name= request.POST['relative_first_name']
                        emp.emergency_contact.last_name= request.POST['relative_last_name']
                        emp.emergency_contact.relation= request.POST['relation']
                        emp.emergency_contact.mobile= request.POST['relative_mobile']
                        emp.emergency_contact.save()
                    else:
                        emp.emergency_contact = EmergencyContact.objects.create(
                            first_name=request.POST['relative_first_name'], \
                            last_name=request.POST['relative_last_name'], \
                            relation=request.POST['relation'], mobile=request.POST['mobile'], )
                        emp.save()
                except Exception as e:
                    logger.error("{}, error occured while saving emergency contact of an employee.".format(e))
                    messages.error(request, "Error occured while saving emergency contact of an employee.")
                    return redirect('update_employee', pk)

        if request.POST['bank_name'] and request.POST['bank_routing_no'] and \
                request.POST['account_no'] and request.POST['account_type']:
            try:
                if emp.bank_account_info:
                    emp.bank_account_info.bank_name = request.POST['bank_name']
                    emp.bank_account_info.bank_routing_no = request.POST['bank_routing_no']
                    emp.bank_account_info.account_no = request.POST['account_no']
                    emp.bank_account_info.account_type = request.POST['account_type']
                    emp.bank_account_info.save()
                else:
                    emp.bank_account_info = BankAccountInfo.objects.create(bank_name=request.POST['bank_name'], \
                                                                           bank_routing_no=request.POST['bank_routing_no'], \
                                                                           account_no=request.POST['account_no'],
                                                                           account_type=request.POST['account_type'], )
                    emp.save()
            except Exception as e:
                logger.error("{}, error occured while saving bank information of an employee.".format(e))
                messages.error(request, "Error occured while saving bank information of an employee.")
                return redirect('update_employee', pk)

        if request.POST['filling_status'] and request.POST['withholding_allowance']:
            try:
                if emp.tax_info:
                    emp.tax_info.filling_status = request.POST['filling_status']
                    emp.tax_info.withholding_allowance = request.POST['withholding_allowance']
                    emp.tax_info.additional_withholding = request.POST['additional_withholding']
                    emp.tax_info.is_withholding_declare = 'is_withholding_declare' in request.POST
                    emp.tax_info.save()
                else:
                    emp.tax_info = TaxInfo.objects.create(filling_status=request.POST['filling_status'], \
                                                            withholding_allowance=request.POST['withholding_allowance'], \
                                                            additional_withholding=request.POST['additional_withholding'],\
                                                            is_withholding_declare= 'is_withholding_declare' in request.POST,)
                    emp.save()
            except Exception as e:
                logger.error("{}, error occured while saving tax information of an employee.".format(e))
                messages.error(request, "Error occured while saving tax information of an employee.")
                return redirect('update_employee', pk)

        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_employee', pk)
        return HttpResponseRedirect(reverse('list_employees'))


class DeleteEmployeeView(LoginRequiredMixin, DeleteView):
    """
    Delete existing employee
    """
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('list_employees')


class UploadEmployeeDocView(LoginRequiredMixin, View):
    """
    Document upload for an emp
    """
    def get(self, request):
        form = EmployeeDocumentForm()
        return render(request, 'upload_employee_docs.html', {'form': form})

    def post(self, request):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        emp_docs = EmployeeDocument.objects.filter(employee=request.POST['employee'])
        document_list = []
        for doc in emp_docs:
            if doc.document:
                document_list.append({'pk': doc.id,
                                     'doc': str(request.build_absolute_uri('/')+'media/'+request.build_absolute_uri('/')[7:-6]+'/'+str(doc.document)),
                                     'name': doc.name,
                                      'description': doc.description})
        return render(request, 'upload_employee_docs.html', {'form': form, 'document_list': document_list})


class DeleteEmployeeDocument(View):
    """
       Delete document of emp
    """

    def get(self, request, pk):
        """
        delete document
        """
        try:
            emp_doc = EmployeeDocument.objects.get(id=int(pk))
            doc_name = emp_doc.name
            emp_doc.delete()
            messages.info(request, doc_name+" document is deleted successfully.")
        except Exception as e:
            logger.error("{}, error occured while deleting document of employee.".format(e))
            messages.error(request, "Error occured while deleting document of employee.")
        form = EmployeeDocumentForm()
        emp_docs = EmployeeDocument.objects.filter(employee= emp_doc.employee)
        document_list = []
        for doc in emp_docs:
            if doc.document:
                document_list.append({'pk': doc.id,
                                     'doc': str(request.build_absolute_uri('/')+'media/'+request.build_absolute_uri('/')[7:-6]+'/'+str(doc.document)),
                                     'name': doc.name,
                                      'description': doc.description})
        return render(request, 'upload_employee_docs.html', {'form': form, 'document_list': document_list})


class ListProjectsView(LoginRequiredMixin, ListView):
    """
    List Projects
    """
    model = Project
    queryset = Project.objects.exclude(status='Delete')
    template_name = 'project_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        queryset = Project.objects.exclude(status='Delete')
        if not self.request.user.is_superuser:
            project_ids = ProjectMembership.objects.filter(employee=self.request.user.employee).values_list('project', flat=False)
            queryset = Project.objects.filter(id__in=project_ids).exclude(status='Delete')
        return queryset


class CreateProjectView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new project
    """
    model = Project
    fields = ['name', 'owner', 'description', 'status', 'note', 'project_activities']
    template_name = 'project_form.html'
    success_message = "%(name)s was created successfully"
    success_url = reverse_lazy('list_projects')

    def get_context_data(self, **kwargs):
        data = super(CreateProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['members'] = ProjectMembershipFormSet(self.request.POST)
        else:
            data['members'] = ProjectMembershipFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        members = context['members']

        with transaction.atomic():
            self.object = form.save()

            if members.is_valid():
                members.instance = self.object
                members.save()
            else:
                logger.error(members.errors)
                messages.error(self.request, members.errors)
                return redirect('add_project')
        return super(CreateProjectView, self).form_valid(form)


class UpdateProjectView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    """
    Update existing project
    """
    model = Project
    fields = ['name', 'owner', 'description', 'status', 'note', 'project_activities']
    template_name = 'project_form.html'
    success_message = "%(name)s was updated successfully"
    success_url = reverse_lazy('list_projects')

    def get_context_data(self, **kwargs):
        data = super(UpdateProjectView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['members'] = ProjectMembershipFormSet(self.request.POST, instance=self.object)
            data['members'].full_clean()
        else:
            data['members'] = ProjectMembershipFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        members = context['members']

        with transaction.atomic():
            self.object = form.save()

            if members.is_valid():
                members.instance = self.object
                members.save()
            else:
                logger.error(members.errors)
                messages.error(self.request, members.errors)
                return redirect('update_project', self.object.id)

        return super(UpdateProjectView, self).form_valid(form)


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    """
    Delete existing project
    """
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('list_projects')


class UploadProjectDocView(LoginRequiredMixin, View):
    """
    Document upload for a project
    """
    def get(self, request):
        form = ProjectDocumentForm()
        return render(request, 'upload_project_docs.html', {'form': form})

    def post(self, request):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = ProjectDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        project_docs = ProjectDocument.objects.filter(project=request.POST['project'])
        document_list = []
        for doc in project_docs:
            if doc.document:
                document_list.append({'pk': doc.id,
                                     'doc': str(request.build_absolute_uri('/')+'media/'+request.build_absolute_uri('/')[7:-6]+'/'+str(doc.document)),
                                     'name': doc.name,
                                      'description': doc.description})
        return render(request, 'upload_project_docs.html', {'form': form, 'document_list': document_list})


class DeleteProjectDocument(View):
    """
       Delete document of project
    """

    def get(self, request, pk):
        """
        delete document
        """
        try:
            project_doc = ProjectDocument.objects.get(id=int(pk))
            doc_name = project_doc.name
            project_doc.delete()
            messages.info(request, doc_name+" document is deleted successfully.")
        except Exception as e:
            logger.error("{}, error occured while deleting document of project.".format(e))
            messages.error(request, "Error occured while deleting document of project.")
        form = ProjectDocumentForm()
        project_docs = ProjectDocument.objects.filter(project= project_doc.project)
        document_list = []
        for doc in project_docs:
            if doc.document:
                document_list.append({'pk': doc.id,
                                     'doc': str(request.build_absolute_uri('/')+'media/'+request.build_absolute_uri('/')[7:-6]+'/'+str(doc.document)),
                                     'name': doc.name,
                                      'description': doc.description})
        return render(request, 'upload_project_docs.html', {'form': form, 'document_list': document_list})


class ListContractsView(LoginRequiredMixin, ListView):
    """
    List Contracts
    """
    model = Contract
    queryset = Contract.objects.exclude(status='Delete')
    template_name = 'contract_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        if self.request.user.is_superuser:
            queryset = Contract.objects.exclude(status='Delete')
        elif not self.request.user.is_superuser and self.request.user.is_staff:
            queryset = Contract.objects.filter(representative=self.request.user.employee)
        else:
            queryset = Contract.objects.filter(employee=self.request.user.employee)
        return queryset


class CreateContractView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new contract
    """
    model = Contract
    fields = ['representative', 'client', 'employee', 'role', 'start_date', 'end_date', 'duration_per_day', 'pay_rate_type',\
              'pay_rate', 'billing_cycle', 'document', 'remark', 'referral', 'status']
    template_name = 'contract_form.html'
    success_message = "contract was created successfully"
    success_url = reverse_lazy('list_contracts')


class UpdateContractView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing contract
    """
    model = Contract
    fields = ['representative', 'client', 'employee', 'role', 'start_date', 'end_date', 'duration_per_day', 'pay_rate_type',\
              'pay_rate', 'billing_cycle', 'document', 'remark', 'referral', 'status']
    template_name = 'contract_form.html'
    success_message = "contract was updated successfully"
    success_url = reverse_lazy('list_contracts')


class DeleteContractView(LoginRequiredMixin, DeleteView):
    """
    Delete existing contract
    """
    model = Contract
    template_name = 'contract_confirm_delete.html'
    success_url = reverse_lazy('list_contracts')


class ListAssignmentsView(LoginRequiredMixin, ListView):
    """
    List Assignments
    """
    model = Assignment
    queryset = Assignment.objects.exclude(status='Delete')
    template_name = 'assignments_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        if self.request.user.is_superuser:
            queryset = Assignment.objects.exclude(status='Delete')
        elif not self.request.user.is_superuser and self.request.user.is_staff:
            queryset = Assignment.objects.filter(created_by=self.request.user)
        else:
            queryset = Assignment.objects.filter(emp=self.request.user.employee)
        return queryset


class CreateAssignmentView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new assignment
    """
    model = Assignment
    fields = ['activity', 'note', 'document', 'emp', 'due_date', 'status']
    template_name = 'assignment_form.html'
    success_message = "Assignment was created successfully"
    success_url = reverse_lazy('list_assignments')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CreateAssignmentView, self).form_valid(form)


class UpdateAssignmentView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing assignment
    """
    model = Assignment
    fields = ['activity', 'note', 'document', 'emp', 'due_date', 'status']
    template_name = 'assignment_form.html'
    success_message = "Assignment was updated successfully"
    success_url = reverse_lazy('list_assignments')


class DeleteAssignmentView(LoginRequiredMixin, DeleteView):
    """
    Delete existing assignment
    """
    model = Assignment
    template_name = 'assignment_confirm_delete.html'
    success_url = reverse_lazy('list_assignments')


class ListTimesheetsView(LoginRequiredMixin, ListView):
    """
    List Timesheets
    """
    model = Timesheet
    queryset = Timesheet.objects.exclude(status='Delete')
    template_name = 'timesheet_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        contract_ids = []
        if self.request.user.is_superuser:
            queryset = Timesheet.objects.exclude(status='Delete')
        elif not self.request.user.is_superuser and self.request.user.is_staff:
            contract_ids = (Contract.objects.filter(representative=self.request.user.employee) | Contract.objects.filter(employee=self.request.user.employee)).distinct()
            queryset = Timesheet.objects.filter(contract__in=contract_ids.values_list('id', flat=False))
        else:
            contract_ids = Contract.objects.filter(employee=self.request.user.employee).values_list('id', flat=True)
            queryset = Timesheet.objects.filter(contract__in=contract_ids)
        return queryset


class CreateTimesheetView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new timesheet
    """
    model = Timesheet
    fields = ['contract', 'remark', 'sign_in', 'sign_out', 'document', 'status']
    template_name = 'timesheet_form.html'
    success_message = "timesheet was created successfully"
    success_url = reverse_lazy('list_timesheets')

    def get_context_data(self, **kwargs):
        data = super(CreateTimesheetView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['tasks'] = TimesheetTaskFormSet(self.request.POST)
        else:
            data['tasks'] = TimesheetTaskFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tasks = context['tasks']
        with transaction.atomic():
            self.object = form.save()
            if tasks.is_valid():
                tasks.instance = self.object
                tasks.save()
            else:
                logger.error(tasks.errors)
                messages.error(self.request, tasks.errors)
                return redirect('add_timesheet')
        return super(CreateTimesheetView, self).form_valid(form)


class UpdateTimesheetView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing timesheet
    """
    model = Timesheet
    fields = ['contract', 'remark', 'sign_in', 'sign_out', 'document', 'status']
    template_name = 'timesheet_form.html'
    success_message = "timesheet was updated successfully"
    success_url = reverse_lazy('list_timesheets')

    def get_context_data(self, **kwargs):
        data = super(UpdateTimesheetView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['tasks'] = TimesheetTaskFormSet(self.request.POST, instance=self.object)
            data['tasks'].full_clean()
        else:
            data['tasks'] = TimesheetTaskFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tasks = context['tasks']
        with transaction.atomic():
            self.object = form.save()
            if tasks.is_valid():
                tasks.instance = self.object
                tasks.save()
            else:
                logger.error(tasks.errors)
                messages.error(self.request, tasks.errors)
                return redirect('update_timesheet', self.object.id)
        return super(UpdateTimesheetView, self).form_valid(form)


class DeleteTimesheetView(LoginRequiredMixin, DeleteView):
    """
    Delete existing timesheet
    """
    model = Timesheet
    template_name = 'timesheet_confirm_delete.html'
    success_url = reverse_lazy('list_timesheets')


class GenericTimesheetView(View):

    def get(self, request):
        return render(request, 'generic_timesheet.html')

    def post(self, request):
        try:
            for d in request.POST['dates'].split(','):
                contract = Contract.objects.get(id=request.POST['contract'])
                start = datetime.strptime(d.strip()+' '+request.POST['start_time'],'%Y-%m-%d %H:%M')
                end = datetime.strptime(d.strip()+' '+request.POST['end_time'], '%Y-%m-%d %H:%M')
                t = Timesheet.objects.create(contract=contract, sign_in=start, sign_out=end,\
                                              remark=request.POST['remark'], status=request.POST['status'])
                if request.FILES:
                    t.document = request.FILES['document']
                    t.save()
            return redirect('list_timesheets')
        except Exception as inst:
            logger.error('Failed to save a timesheets in generic by user {}'.format(request.user.username))
            messages.error(request, 'Error occured while saving timesheets.')
            return redirect('add_generic_timesheet')


class ListVendorsView(LoginRequiredMixin, ListView):
    """
    List vendors
    """
    model = Vendor
    queryset = Vendor.objects.exclude(status='Delete')
    template_name = 'vendor_list.html'


class CreateVendorView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new vendor
    """
    model = Vendor
    fields = ['organization_name', 'contact_person_name', 'designation', 'mobile', 'email', 'note', 'status']
    template_name = 'vendor_form.html'
    success_message = "%(organization_name)s was created successfully"
    success_url = reverse_lazy('list_vendors')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            vendor = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            if city and country and state and zip_code:
                try:
                    vendor.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state,\
                                                            country=country,zip_code=int(zip_code))
                    vendor.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of a vendor.".format(e))
                    messages.error(request, "Error occured while saving address of a vendor.")
                    return redirect('add_vendor')
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_vendor')
        return HttpResponseRedirect(reverse('list_vendors'))


class UpdateVendorView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing vendor
    """
    model = Vendor
    fields = ['organization_name', 'contact_person_name', 'designation', 'mobile', 'email', 'note', 'status']
    template_name = 'edit_vendor_form.html'
    success_message = "%(organization_name)s was updated successfully"
    success_url = reverse_lazy('list_vendors')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Vendor.objects.get(id=pk)
        return render(request, 'edit_vendor_form.html', {'obj': obj})

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Vendor.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            vendor = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']

            if city and country and state and zip_code:
                try:
                    if vendor.address:
                        vendor.address.line1=line1
                        vendor.address.line2=line2
                        vendor.address.city_or_village=city
                        vendor.address.state=state
                        vendor.address.country=country
                        vendor.address.zip_code=int(zip_code)
                        vendor.address.save()
                    else:
                        vendor.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city,
                                                                state=state, country=country, zip_code=int(zip_code))
                        vendor.save()

                except Exception as e:
                    logger.error("{}, error occured while saving address of a vendor.".format(e))
                    messages.error(request, "Error occured while saving address of a vendor.")
                    return redirect('update_vendor', pk)
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_vendor', pk)
        return HttpResponseRedirect(reverse('list_vendors'))


class DeleteVendorView(LoginRequiredMixin, DeleteView):
    """
    Delete existing vendor
    """
    model = Vendor
    template_name = 'vendor_confirm_delete.html'
    success_url = reverse_lazy('list_vendors')


class UploadVendorDocView(LoginRequiredMixin, View):
    """
    Document upload for a vendor
    """
    def get(self, request):
        form = VendorDocumentForm()
        return render(request, 'upload_vendor_docs.html', {'form': form})

    def post(self, request):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = VendorDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        vendor_docs = VendorDocument.objects.filter(vendor=request.POST['vendor'])
        document_list = []
        for doc in vendor_docs:
            if doc.document:
                document_list.append({'pk': doc.id,
                                     'doc': str(request.build_absolute_uri('/')+'media/'+request.build_absolute_uri('/')[7:-6]+'/'+str(doc.document)),
                                     'name': doc.name,
                                      'description': doc.description})
        return render(request, 'upload_vendor_docs.html', {'form': form, 'document_list': document_list})


class DeleteVendorDocument(View):
    """
       Delete document of vendor
    """

    def get(self, request, pk):
        """
        delete document
        """
        try:
            vendor_doc = VendorDocument.objects.get(id=int(pk))
            doc_name = vendor_doc.name
            vendor_doc.delete()
            messages.info(request, doc_name+" document is deleted successfully.")
        except Exception as e:
            logger.error("{}, error occured while deleting document of vendor.".format(e))
            messages.error(request, "Error occured while deleting document of vendor.")
        form = VendorDocumentForm()
        vendor_docs = VendorDocument.objects.filter(vendor= vendor_doc.vendor)
        document_list = []
        for doc in vendor_docs:
            if doc.document:
                document_list.append({'pk': doc.id,
                                     'doc': str(request.build_absolute_uri('/')+'media/'+request.build_absolute_uri('/')[7:-6]+'/'+str(doc.document)),
                                     'name': doc.name,
                                      'description': doc.description})
        return render(request, 'upload_vendor_docs.html', {'form': form, 'document_list': document_list})


class ListReferralsView(LoginRequiredMixin, ListView):
    """
    List referrals
    """
    model = Referral
    queryset = Referral.objects.exclude(status='Delete')
    template_name = 'referrals_list.html'


class CreateReferralView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new referral
    """
    model = Referral
    fields = ['first_name', 'last_name', 'mobile', 'email', 'document', 'emp']
    template_name = 'referral_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_referrals')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            referral = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            if city and country and state and zip_code:
                try:
                    referral.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state,\
                                                            country=country,zip_code=int(zip_code))
                    referral.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of a referral.".format(e))
                    messages.error(request, "Error occured while saving address of a referral.")
                    return redirect('add_referral')
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_referral')
        return HttpResponseRedirect(reverse('list_referrals'))


class UpdateReferralView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing referral
    """
    model = Referral
    fields = ['first_name', 'last_name', 'mobile', 'email', 'document', 'emp']
    template_name = 'edit_referral_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_referrals')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Referral.objects.get(id=pk)
        form = self.get_form()
        if self.object.document:
            file_url = request.build_absolute_uri('/')[:-1]+self.object.document.url
        else:
            file_url=''
        return render(request, 'edit_referral_form.html', {'form': form, 'obj': self.object, 'file_url':file_url})

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Referral.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            referral = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']

            if city and country and state and zip_code:
                try:
                    if referral.address:
                        referral.address.line1=line1
                        referral.address.line2=line2
                        referral.address.city_or_village=city
                        referral.address.state=state
                        referral.address.country=country
                        referral.address.zip_code=int(zip_code)
                        referral.address.save()
                    else:
                        referral.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city,
                                                                state=state, country=country, zip_code=int(zip_code))
                        referral.save()

                except Exception as e:
                    logger.error("{}, error occured while saving address of a referral.".format(e))
                    messages.error(request, "Error occured while saving address of a referral.")
                    return redirect('update_referral', pk)
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_referral', pk)
        return HttpResponseRedirect(reverse('list_referrals'))


class DeleteReferralView(LoginRequiredMixin, DeleteView):
    """
    Delete existing referral
    """
    model = Referral
    template_name = 'referral_confirm_delete.html'
    success_url = reverse_lazy('list_referrals')


class ReportView(LoginRequiredMixin, View):
    """
    Report
    """
    def get(self, request):
        """
          report
        """
        form = SearchForm()
        emps = Employee.objects.exclude(status='Delete').order_by('first_name')
        return render(request, 'search_form.html', {'form': form, 'emps':emps})

    def post(self, request):
        try:
            form = SearchForm(request.POST)
            emps = Employee.objects.exclude(status='Delete').order_by('first_name')

            if form.is_valid():
                list_contracts = get_report_data(form.cleaned_data['resource_name'], form.cleaned_data['from_date'],\
                                                 form.cleaned_data['to_date'])
                if 'submit_btn' in request.POST:
                    return render(request, 'search_form.html', {'form':form, 'list_contracts': list_contracts})
                else:
                    return Render.pdf_file('report.html', {'list_contracts': list_contracts,\
                                                'emp_name': form.cleaned_data['resource_name'],\
                                                'from_date': form.cleaned_data['from_date'],\
                                                'to_date': form.cleaned_data['to_date']})
            else:
                return render(request, 'search_form.html', {'form': form, 'emps':emps, 'messages': form.errors})
        except Exception as e:
            logger.error("{}, error occured while searching report.".format(e))
            messages.error(request, "Error occured while searching report.")
            return redirect('report')


class ExpenseReportView(LoginRequiredMixin, View):
    """
    Expense Report
    """
    def get(self, request):
        form = SearchForm()
        emps = Employee.objects.exclude(status='Delete').order_by('first_name')
        return render(request, 'search_expense_report.html', {'form': form, 'emps':emps})

    def post(self, request):
        try:
            form = SearchForm(request.POST)
            emps = Employee.objects.exclude(status='Delete').order_by('first_name')

            if form.is_valid():
                result = get_expense_report(form.cleaned_data['resource_name'], form.cleaned_data['from_date'],\
                                                 form.cleaned_data['to_date'])

                return render(request, 'search_expense_report.html', {'form':form, 'emps':emps, 'result': result})
            else:
                return render(request, 'search_expense_report.html', {'form': form, 'emps':emps, 'messages': form.errors})
        except Exception as e:
            logger.error("{}, error occured while searching expense report.".format(e))
            messages.error(request, "Error occured while searching expense report.")
            return redirect('expense_report')


class SearchDefaulterView(LoginRequiredMixin, View):
    """
    Get defaulters
    """
    def get(self, request):
        """
          Get defaulters
        """
        form = SearchForm()
        emps = Employee.objects.exclude(status='Delete').order_by('first_name')
        return render(request, 'search_defaulter_form.html', {'form': form, 'emps':emps})

    def post(self, request):
        try:
            form = SearchForm(request.POST)
            emps = Employee.objects.exclude(status='Delete').order_by('first_name')

            if form.is_valid():
                list_contracts = get_defaulter(form.cleaned_data['resource_name'], form.cleaned_data['from_date'],\
                                                 form.cleaned_data['to_date'])
                if list_contracts:
                    return render(request, 'search_defaulter_form.html', {'form': form, 'emps':emps,\
                                                                          'list_contracts': list_contracts})
                else:
                    return render(request, 'search_defaulter_form.html', {'form': form, 'emps':emps,\
                                                                          'message': str("Not  defaulter")})
            else:
                return render(request, 'search_defaulter_form.html', {'form': form, 'emps':emps,\
                                                                      'message': form.errors})
        except Exception as e:
            logger.error("{}, error occured while searching defaulters.".format(e))
            messages.error(request, "Error occured while searching defaulters.")
            return redirect('get_defaulters')


class InboxMessagesView(LoginRequiredMixin, View):
    """
    List messages
    """
    def get(self, request):
        if self.request.user.is_staff:
            queryset = Message.objects.all()
        else:
            queryset = Message.objects.filter(receiver=self.request.user)
        return render(request, 'message_inbox.html', {'inbox_messages': queryset})


class CreateMessageView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new message
    """
    model = Message
    fields = ['receiver', 'note']
    template_name = 'message_form.html'
    success_message = "Message was created successfully"
    success_url = reverse_lazy('inbox_messages')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(CreateMessageView, self).form_valid(form)


class UpdateMessageView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing message
    """
    model = Message
    fields = ['receiver', 'note']
    template_name = 'message_form.html'
    success_message = "Message was updated successfully"
    success_url = reverse_lazy('inbox_messages')


class DeleteMessageView(LoginRequiredMixin, DeleteView):
    """
    Delete existing message
    """
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('inbox_messages')


class ListTasksView(LoginRequiredMixin, ListView):
    """
    List Tasks
    """
    model = Task
    queryset = Task.objects.exclude(status='Delete')
    template_name = 'tasks_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        if self.request.user.is_superuser:
            queryset = Task.objects.exclude(status='Delete')
        elif not self.request.user.is_superuser and self.request.user.is_staff:
            queryset = Task.objects.filter(created_by=self.request.user)
        else:
            queryset = Task.objects.filter(emps__id__in=[self.request.user.employee.id])
        return queryset


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new task
    """
    model = Task
    fields = ['task_name', 'due_date', 'description', 'emps', 'status']
    template_name = 'task_form.html'
    success_message = "Task was created successfully"
    success_url = reverse_lazy('list_tasks')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CreateTaskView, self).form_valid(form)


class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing task
    """
    model = Task
    fields = ['task_name', 'due_date', 'description', 'emps', 'status']
    template_name = 'task_form.html'
    success_message = "Task was updated successfully"
    success_url = reverse_lazy('list_tasks')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    """
    Delete existing task
    """
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('list_tasks')


class ListEmpExpensesView(LoginRequiredMixin, View):
    """
    List expenses of an employee
    """
    def get(self, request, emp_id):
        emp = Employee.objects.get(id=emp_id)
        employee_expenses = EmployeeExpense.objects.filter(employee=emp).exclude(status='Delete')
        return render(request, 'emp_expense_list.html', {'employee_expenses': employee_expenses, "emp": emp})


class CreateEmpExpenseView(LoginRequiredMixin, SuccessMessageMixin, View):
    """
    Add new expense of an employee
    """
    def get(self, request, emp_id):
        form = EmployeeExpenseForm(initial = {"employee": emp_id})
        return render(request, 'emp_expense_form.html', {'form': form, 'emp_id': emp_id})

    def post(self, request, emp_id):
        form = EmployeeExpenseForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'emp_expense_form.html', {'form': form, 'emp_id': emp_id, 'messages':form.errors})
        return HttpResponseRedirect(reverse('list_emp_expenses',  kwargs={'emp_id':emp_id}))


class UpdateEmpExpenseView(LoginRequiredMixin,SuccessMessageMixin, View):
    """
    Update existing expense record
    """
    def get(self, request, emp_id, expense_id):
        obj = EmployeeExpense.objects.get(id=expense_id)
        form = EmployeeExpenseForm(instance=obj)
        return render(request, 'emp_expense_form.html', {'form': form, 'emp_id': emp_id})

    def post(self, request, emp_id, expense_id):
        obj = EmployeeExpense.objects.get(id=expense_id)
        form = EmployeeExpenseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'emp_expense_form.html', {'form': form, 'emp_id': emp_id, 'messages':form.errors})
        return HttpResponseRedirect(reverse('list_emp_expenses',  kwargs={'emp_id':emp_id}))


class DeleteEmpExpenseView(LoginRequiredMixin, View):
    """
    Delete existing expense record
    """
    def get(self, request, emp_id, expense_id):
        obj = EmployeeExpense.objects.get(id=expense_id)
        return render(request, 'emp_expense_confirm_delete.html', {'emp_id': emp_id,'obj': obj})

    def post(self, request, emp_id, expense_id):
        obj = EmployeeExpense.objects.get(id=expense_id)
        obj.status = 'Delete'
        obj.save()
        return HttpResponseRedirect(reverse('list_emp_expenses',  kwargs={'emp_id':emp_id}))


class ListVendorExpensesView(LoginRequiredMixin, View):
    """
    List expenses of a vendor
    """
    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(id=vendor_id)
        vendor_expenses = VendorExpense.objects.filter(vendor=vendor).exclude(status='Delete')
        return render(request, 'vendor_expense_list.html', {'vendor_expenses': vendor_expenses, "vendor": vendor})


class CreateVendorExpenseView(LoginRequiredMixin, SuccessMessageMixin, View):
    """
    Add new expense of a vendor
    """
    def get(self, request, vendor_id):
        form = VendorExpenseForm(initial = {"vendor": vendor_id})
        return render(request, 'vendor_expense_form.html', {'form': form, 'vendor_id': vendor_id})

    def post(self, request, vendor_id):
        form = VendorExpenseForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'vendor_expense_form.html', {'form': form, 'vendor_id': vendor_id, 'messages':form.errors})
        return HttpResponseRedirect(reverse('list_vendor_expenses',  kwargs={'vendor_id':vendor_id}))


class UpdateVendorExpenseView(LoginRequiredMixin,SuccessMessageMixin, View):
    """
    Update existing expense record
    """
    def get(self, request, vendor_id, expense_id):
        obj = VendorExpense.objects.get(id=expense_id)
        form = VendorExpenseForm(instance=obj)
        return render(request, 'vendor_expense_form.html', {'form': form, 'vendor_id': vendor_id})

    def post(self, request, vendor_id, expense_id):
        obj = VendorExpense.objects.get(id=expense_id)
        form = VendorExpenseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'vendor_expense_form.html', {'form': form, 'vendor_id': vendor_id, 'messages':form.errors})
        return HttpResponseRedirect(reverse('list_vendor_expenses',  kwargs={'vendor_id':vendor_id}))


class DeleteVendorExpenseView(LoginRequiredMixin, View):
    """
    Delete existing expense record
    """
    def get(self, request, vendor_id, expense_id):
        obj = VendorExpense.objects.get(id=expense_id)
        return render(request, 'vendor_expense_confirm_delete.html', {'vendor_id': vendor_id,'obj': obj})

    def post(self, request, vendor_id, expense_id):
        obj = VendorExpense.objects.get(id=expense_id)
        obj.status = 'Delete'
        obj.save()
        return HttpResponseRedirect(reverse('list_vendor_expenses',  kwargs={'vendor_id':vendor_id}))


class ListProjectExpensesView(LoginRequiredMixin, View):
    """
    List expenses of a project
    """
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project_expenses = ProjectExpense.objects.filter(project=project).exclude(status='Delete')
        return render(request, 'project_expense_list.html', {'project_expenses': project_expenses, "project": project})


class CreateProjectExpenseView(LoginRequiredMixin, SuccessMessageMixin, View):
    """
    Add new expense of a project
    """
    def get(self, request, project_id):
        form = ProjectExpenseForm(initial = {"project": project_id})
        return render(request, 'project_expense_form.html', {'form': form, 'project_id': project_id})

    def post(self, request, project_id):
        form = ProjectExpenseForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'project_expense_form.html', {'form': form, 'project_id': project_id, 'messages':form.errors})
        return HttpResponseRedirect(reverse('list_project_expenses',  kwargs={'project_id':project_id}))


class UpdateProjectExpenseView(LoginRequiredMixin,SuccessMessageMixin, View):
    """
    Update existing expense record
    """
    def get(self, request, project_id, expense_id):
        obj = ProjectExpense.objects.get(id=expense_id)
        form = ProjectExpenseForm(instance=obj)
        return render(request, 'project_expense_form.html', {'form': form, 'project_id': project_id})

    def post(self, request, project_id, expense_id):
        obj = ProjectExpense.objects.get(id=expense_id)
        form = ProjectExpenseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'project_expense_form.html', {'form': form, 'project_id': project_id, 'messages':form.errors})
        return HttpResponseRedirect(reverse('list_project_expenses',  kwargs={'project_id':project_id}))


class DeleteProjectExpenseView(LoginRequiredMixin, View):
    """
    Delete existing expense record
    """
    def get(self, request, project_id, expense_id):
        obj = ProjectExpense.objects.get(id=expense_id)
        return render(request, 'project_expense_confirm_delete.html', {'project_id': project_id,'obj': obj})

    def post(self, request, project_id, expense_id):
        obj = ProjectExpense.objects.get(id=expense_id)
        obj.status = 'Delete'
        obj.save()
        return HttpResponseRedirect(reverse('list_project_expenses',  kwargs={'project_id':project_id}))


class ListInvoicesView(LoginRequiredMixin, ListView):
    """
    List Invoices
    """
    model = Invoice
    queryset = Invoice.objects.exclude(status='Delete')
    template_name = 'invoice_list.html'


class CreateInvoiceView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new invoice
    """
    model = Invoice
    fields = ['client', 'due_date', 'tax', 'discount', 'final_amount', 'document', 'remark', 'status', 'credits', 'balance']
    template_name = 'invoice_form.html'
    success_message = "Invoice was created successfully"
    success_url = reverse_lazy('list_invoices')

    def get_context_data(self, **kwargs):
        data = super(CreateInvoiceView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = InvoiceItemFormSet(self.request.POST)
        else:
            data['items'] = InvoiceItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.instance = self.object
                items.save()
            else:
                logger.error(items.errors)
                messages.error(self.request, items.errors)
                return redirect('add_invoice')
        return super(CreateInvoiceView, self).form_valid(form)


class UpdateInvoiceView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing invoice
    """
    model = Invoice
    fields =  ['client', 'due_date', 'tax', 'discount', 'final_amount', 'document', 'remark', 'status', 'credits', 'balance']
    template_name = 'invoice_form.html'
    success_message = "Invoice was updated successfully"
    success_url = reverse_lazy('list_invoices')

    def get_context_data(self, **kwargs):
        data = super(UpdateInvoiceView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = InvoiceItemFormSet(self.request.POST, instance=self.object)
            data['items'].full_clean()
        else:
            data['items'] = InvoiceItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.instance = self.object
                items.save()
            else:
                logger.error(items.errors)
                messages.error(self.request, items.errors)
                return redirect('update_invoice', self.object.id)
        return super(UpdateInvoiceView, self).form_valid(form)


class DeleteInvoiceView(LoginRequiredMixin, DeleteView):
    """
    Delete existing invoice
    """
    model = Invoice
    template_name = 'invoice_confirm_delete.html'
    success_url = reverse_lazy('list_invoices')


class SendInvoiceView(LoginRequiredMixin, View):
    """
    Send invoice to a client
    """
    def get(self, request, pk):
        invoice = Invoice.objects.get(id=pk)
        services = InvoiceItem.objects.filter(invoice=invoice)
        if Render.send_invoice('client_invoice.html', {'invoice': invoice, 'services':services }, invoice.client.email, str(invoice.document)):
            messages.success(request, "Invoice sucessfully sent to a client's email.")
        else:
            messages.error(request, "Error occured while sending invoice.")
        return redirect('update_invoice', pk)
