import logging

from datetime import datetime

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

logger = logging.getLogger('tracker_log')


class DashboardView(LoginRequiredMixin, View):
    """
    Dashboard
    """
    def get(self, request):
        """
          dashboard
        """
        data = { "employees_count" : Employee.objects.exclude(status='Delete').count(),
        "clients_count" : Client.objects.exclude(status='Delete').count(),
        "projects_count" : Project.objects.exclude(status='Delete').count(),
        "contracts_count" : Contract.objects.exclude(status='Delete').count()}
        return render(request, 'dashboard.html', data)


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
            # import pdb; pdb.set_trace()
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

   # def post(self, request, pk):
    #    """
     #   Handle POST requests: instantiate a form instance with the passed
      #  POST variables and then check if it's valid.
       # """
        #self.object = User.objects.get(id=pk)
        #form = self.get_form()
        #if form.is_valid():
         #   user = form.save()
          #  user.set_password(request.POST['password'])
           # user.save()
       # else:
        #    pass
        #return HttpResponseRedirect(reverse('list_users'))


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
              'skype_id', 'department', 'designation', 'employment_type','current_pay_rate_type','current_pay_rate',\
              'passport_no','current_visa_status', 'document', 'status']
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
                    emp.tax_info = EmpTaxInfo.objects.create(filling_status=request.POST['filling_status'], \
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
              'skype_id', 'department', 'designation', 'employment_type','current_pay_rate_type','current_pay_rate',\
              'passport_no','current_visa_status', 'document', 'status']
    template_name = 'edit_employee_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_employees')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Employee.objects.get(id=pk)
        if obj.document:
            file_url = request.build_absolute_uri('/')[:-1]+obj.document.url
        else:
            file_url=''
        return render(request, 'edit_employee_form.html', {'obj': obj, 'file_url':file_url})

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
                    emp.tax_info = EmpTaxInfo.objects.create(filling_status=request.POST['filling_status'], \
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


class ListProjectsView(LoginRequiredMixin, ListView):
    """
    List Projects
    """
    model = Project
    queryset = Project.objects.all()
    template_name = 'project_list.html'


class CreateProjectView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new project
    """
    model = Project
    fields = ['name', 'description', 'owner', 'representative', 'document', 'status']
    template_name = 'project_form.html'
    success_message = "%(name)s was created successfully"
    success_url = reverse_lazy('list_projects')


class UpdateProjectView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    """
    Update existing project
    """
    model = Project
    fields = ['name', 'description', 'owner', 'representative', 'document', 'status']
    template_name = 'project_form.html'
    success_message = "%(name)s was updated successfully"
    success_url = reverse_lazy('list_projects')


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    """
    Delete existing project
    """
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('list_projects')


class ListContractsView(LoginRequiredMixin, ListView):
    """
    List Contracts
    """
    model = Contract
    queryset = Contract.objects.all()
    template_name = 'contract_list.html'


class CreateContractView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new contract
    """
    model = Contract
    fields = ['project', 'employee', 'role', 'start_date', 'end_date', 'duration_per_day', 'pay_rate_type',\
              'pay_rate', 'billing_cycle', 'remark', 'document', 'status']
    template_name = 'contract_form.html'
    success_message = "contract was created successfully"
    success_url = reverse_lazy('list_contracts')


class UpdateContractView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing contract
    """
    model = Contract
    fields = ['project', 'employee', 'role', 'start_date', 'end_date', 'duration_per_day', 'pay_rate_type',\
              'pay_rate', 'billing_cycle', 'remark', 'document', 'status']
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


class ListTasksView(LoginRequiredMixin, ListView):
    """
    List Tasks
    """
    model = TaskAllocation
    queryset = TaskAllocation.objects.exclude(status='Delete')
    template_name = 'tasks_list.html'


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new task
    """
    model = TaskAllocation
    fields = ['title', 'description', 'due_date','emp', 'document', 'status']
    template_name = 'task_form.html'
    success_message = "task was created successfully"
    success_url = reverse_lazy('list_tasks')


class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing task
    """
    model = TaskAllocation
    fields = ['title', 'description', 'due_date', 'emp', 'document', 'status']
    template_name = 'task_form.html'
    success_message = "task was updated successfully"
    success_url = reverse_lazy('list_tasks')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    """
    Delete existing task
    """
    model = TaskAllocation
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('list_tasks')


class ListTimesheetsView(LoginRequiredMixin, ListView):
    """
    List Timesheets
    """
    model = Timesheet
    queryset = Timesheet.objects.all()
    template_name = 'timesheet_list.html'


class CreateTimesheetView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new timesheet
    """
    model = Timesheet
    fields = ['contract', 'sign_in', 'sign_out','tasks','is_billable', 'document', 'status']
    template_name = 'timesheet_form.html'
    success_message = "timesheet was created successfully"
    success_url = reverse_lazy('list_timesheets')


class UpdateTimesheetView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing timesheet
    """
    model = Timesheet
    fields = ['contract', 'sign_in', 'sign_out','tasks','is_billable', 'document', 'status']
    template_name = 'timesheet_form.html'
    success_message = "timesheet was updated successfully"
    success_url = reverse_lazy('list_timesheets')


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
            if request.POST['is_billable']:
                is_billable = True
            else:
                is_billable = False

            for d in request.POST['dates'].split(','):
                contract = Contract.objects.get(id=request.POST['contract'])
                start = datetime.strptime(d.strip()+' '+request.POST['start_time'],'%Y-%m-%d %H:%M')
                end = datetime.strptime(d.strip()+' '+request.POST['end_time'], '%Y-%m-%d %H:%M')
                t = Timesheet.objects.create(contract=contract, sign_in=start, sign_out=end, tasks=request.POST['tasks'],\
                                         is_billable=is_billable, status=request.POST['status'])
                doc = request.FILES['document']
                if doc:
                    t.document = doc
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
    fields = ['organization_name', 'contact_person_name', 'designation', 'mobile', 'email', 'remark', 'document', 'status']
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
    fields = ['organization_name', 'contact_person_name', 'designation', 'mobile', 'email', 'remark', 'document', 'status']
    template_name = 'edit_vendor_form.html'
    success_message = "%(organization_name)s was updated successfully"
    success_url = reverse_lazy('list_vendors')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Vendor.objects.get(id=pk)
        if obj.document:
            file_url = request.build_absolute_uri('/')[:-1]+obj.document.url
        else:
            file_url=''
        return render(request, 'edit_vendor_form.html', {'obj': obj, 'file_url':file_url})

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
            # import pdb; pdb.set_trace()
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
    fields = ['first_name', 'last_name', 'mobile', 'email', 'document', 'emp', 'status']
    template_name = 'referral_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_referrals')
    #
    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         client = form.save()
    #         line1 = request.POST['line1']
    #         line2 = request.POST['line2']
    #         city = request.POST['location']
    #         country = request.POST['country']
    #         state = request.POST['state']
    #         zip_code = request.POST['zip']
    #         if city and country and state and zip_code:
    #             try:
    #                 client.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state,\
    #                                                         country=country,zip_code=int(zip_code))
    #                 client.save()
    #             except Exception as e:
    #                 logger.error("{}, error occured while saving address of a client.".format(e))
    #                 messages.error(request, "Error occured while saving address of a client.")
    #                 return redirect('add_client')
    #     else:
    #         logger.error(form.errors)
    #         messages.error(request, form.errors)
    #         return redirect('add_client')
    #     return HttpResponseRedirect(reverse('list_clients'))


class UpdateReferralView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing referral
    """
    pass
    # model = Referral
    # fields = ['first_name', 'last_name', 'gender', 'mobile', 'email', 'skype_id', 'document', 'status']
    # template_name = 'edit_client_form.html'
    # success_message = "%(first_name)s was updated successfully"
    # success_url = reverse_lazy('list_clients')
    #
    # def get(self, request, pk):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     obj = Client.objects.get(id=pk)
    #     if obj.document:
    #         file_url = request.build_absolute_uri('/')[:-1]+obj.document.url
    #     else:
    #         file_url=''
    #     return render(request, 'edit_client_form.html', {'obj': obj, 'file_url':file_url})
    #
    # def post(self, request, pk):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     self.object = Client.objects.get(id=pk)
    #     form = self.get_form()
    #     if form.is_valid():
    #         client = form.save()
    #         line1 = request.POST['line1']
    #         line2 = request.POST['line2']
    #         city = request.POST['location']
    #         country = request.POST['country']
    #         state = request.POST['state']
    #         zip_code = request.POST['zip']
    #         # import pdb; pdb.set_trace()
    #         if city and country and state and zip_code:
    #             try:
    #                 if client.address:
    #                     client.address.line1=line1
    #                     client.address.line2=line2
    #                     client.address.city_or_village=city
    #                     client.address.state=state
    #                     client.address.country=country
    #                     client.address.zip_code=int(zip_code)
    #                     client.address.save()
    #                 else:
    #                     client.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city,
    #                                                             state=state, country=country, zip_code=int(zip_code))
    #                     client.save()
    #
    #             except Exception as e:
    #                 logger.error("{}, error occured while saving address of a client.".format(e))
    #                 messages.error(request, "Error occured while saving address of a client.")
    #                 return redirect('update_client', pk)
    #     else:
    #         logger.error(form.errors)
    #         messages.error(request, form.errors)
    #         return redirect('update_client', pk)
    #     return HttpResponseRedirect(reverse('list_clients'))


class DeleteReferralView(LoginRequiredMixin, DeleteView):
    """
    Delete existing referral
    """
    model = Referral
    template_name = 'referral_confirm_delete.html'
    success_url = reverse_lazy('list_referrals')