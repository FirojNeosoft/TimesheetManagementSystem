from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from tracker.models import *

class DashboardView(View):
    """
    Dashboard
    """

    # @login_required
    def get(self, request):
        """
          dashboard
        """
        data = { "employees_count" : Employee.objects.exclude(status='Delete').count(),
        "clients_count" : Client.objects.exclude(status='Delete').count(),
        "projects_count" : Project.objects.exclude(status='Delete').count(),
        "contracts_count" : Contract.objects.exclude(status='Delete').count()}
        return render(request, 'dashboard.html', data)


class ListClientsView(ListView):
    """
    List Clients
    """
    model = Client
    queryset = Client.objects.exclude(status='Delete')
    template_name = 'client_list.html'


class CreateClientView(SuccessMessageMixin, CreateView):
    """
    Create new client
    """
    model = Client
    fields = ['first_name', 'last_name', 'gender', 'mobile', 'email', 'skype_id', 'status']
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
                    client.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state, country=country,zip_code=int(zip_code))
                    client.save()
                except:
                    pass
        else:
            pass
        return HttpResponseRedirect(reverse('list_clients'))


class UpdateClientView(SuccessMessageMixin, UpdateView):
    """
    Update existing client
    """
    model = Client
    fields = ['first_name', 'last_name', 'gender', 'mobile', 'email', 'skype_id', 'status']
    template_name = 'edit_client_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_clients')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Client.objects.get(id=pk)
        return render(request, 'edit_client_form.html', {'obj': obj})

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
                    client.address.line1=line1
                    client.address.line2=line2
                    client.address.city_or_village=city
                    client.address.state=state
                    client.address.country=country
                    client.address.zip_code=int(zip_code)
                    client.address.save()
                except:
                    pass
        else:
            pass
        return HttpResponseRedirect(reverse('list_clients'))


class DeleteClientView(DeleteView):
    """
    Delete existing client
    """
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('list_clients')


class ListUsersView(ListView):
    """
    List Users
    """
    model = User
    queryset = User.objects.all()
    template_name = 'user_list.html'


class CreateUserView(SuccessMessageMixin, CreateView):
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
            pass
        return HttpResponseRedirect(reverse('list_users'))

class UpdateUserView(SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was updated successfully"
    success_url = reverse_lazy('list_users')

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = User.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password'])
            user.save()
        else:
            pass
        return HttpResponseRedirect(reverse('list_users'))

class DeleteUserView(DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('list_users')


class ListEmployeesView(ListView):
    """
    List Employees
    """
    model = Employee
    queryset = Employee.objects.exclude(status='Delete')
    template_name = 'employees_list.html'


class CreateEmployeeView(SuccessMessageMixin, CreateView):
    """
    Create new employee
    """
    model = Employee
    fields = ['first_name', 'last_name', 'employee_id', 'birth_date', 'gender', 'joined_date', 'mobile', 'email',\
              'skype_id', 'department', 'designation', 'employment_type','current_pay_rate_type','current_pay_rate','passport_no','current_visa_status','status']
    template_name = 'employee_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_employees')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        # import pdb; pdb.set_trace()
        if form.is_valid():
            emp = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            if city and country and state and zip_code:
                try:
                    emp.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state, country=country,zip_code=int(zip_code))
                    emp.save()
                except:
                    pass
        else:
            pass
        return HttpResponseRedirect(reverse('list_employees'))


class UpdateEmployeeView(SuccessMessageMixin, UpdateView):
    """
    Update existing employee
    """
    model = Employee
    fields = ['first_name', 'last_name', 'employee_id', 'birth_date', 'gender', 'joined_date', 'mobile', 'email',\
              'skype_id', 'department', 'designation', 'employment_type','current_pay_rate_type','current_pay_rate','passport_no','current_visa_status','status']
    template_name = 'employee_form.html'
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
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            if city and country and state and zip_code:
                try:
                    emp.address.line1=line1
                    emp.address.line2=line2
                    emp.address.city_or_village=city
                    emp.address.state=state
                    emp.address.country=country
                    emp.address.zip_code=int(zip_code)
                    emp.address.save()
                except:
                    pass
        else:
            pass
        return HttpResponseRedirect(reverse('list_employees'))


class DeleteEmployeeView(DeleteView):
    """
    Delete existing employee
    """
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('list_employees')


class ListProjectsView(ListView):
    """
    List Projects
    """
    model = Project
    queryset = Project.objects.all()
    template_name = 'project_list.html'


class CreateProjectView(SuccessMessageMixin, CreateView):
    """
    Create new project
    """
    model = Project
    fields = ['name', 'description', 'owner', 'representative', 'status']
    template_name = 'project_form.html'
    success_message = "%(name)s was created successfully"
    success_url = reverse_lazy('list_projects')


class UpdateProjectView(SuccessMessageMixin, UpdateView):
    """
    Update existing project
    """
    model = Project
    fields = ['name', 'description', 'owner', 'representative', 'status']
    template_name = 'project_form.html'
    success_message = "%(name)s was updated successfully"
    success_url = reverse_lazy('list_projects')


class DeleteProjectView(DeleteView):
    """
    Delete existing project
    """
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('list_projects')


class ListContractsView(ListView):
    """
    List Contracts
    """
    model = Contract
    queryset = Contract.objects.all()
    template_name = 'contract_list.html'


class CreateContractView(SuccessMessageMixin, CreateView):
    """
    Create new contract
    """
    model = Contract
    fields = ['project', 'employee', 'role', 'start_date', 'end_date', 'duration_per_day', 'pay_rate_type',\
              'pay_rate', 'billing_cycle', 'remark', 'status']
    template_name = 'contract_form.html'
    success_message = "contract was created successfully"
    success_url = reverse_lazy('list_contracts')


class UpdateContractView(SuccessMessageMixin, UpdateView):
    """
    Update existing contract
    """
    model = Contract
    fields = ['project', 'employee', 'role', 'start_date', 'end_date', 'duration_per_day', 'pay_rate_type',\
              'pay_rate', 'billing_cycle', 'remark', 'status']
    template_name = 'contract_form.html'
    success_message = "contract was updated successfully"
    success_url = reverse_lazy('list_contracts')


class DeleteContractView(DeleteView):
    """
    Delete existing contract
    """
    model = Contract
    template_name = 'contract_confirm_delete.html'
    success_url = reverse_lazy('list_contracts')


class ListTimesheetsView(ListView):
    """
    List Timesheets
    """
    model = Timesheet
    queryset = Timesheet.objects.all()
    template_name = 'timesheet_list.html'


class CreateTimesheetView(SuccessMessageMixin, CreateView):
    """
    Create new timesheet
    """
    model = Timesheet
    fields = ['contract', 'sign_in', 'sign_out','tasks','is_billable', 'status']
    template_name = 'timesheet_form.html'
    success_message = "timesheet was created successfully"
    success_url = reverse_lazy('list_timesheets')


class UpdateTimesheetView(SuccessMessageMixin, UpdateView):
    """
    Update existing timesheet
    """
    model = Timesheet
    fields = ['contract', 'sign_in', 'sign_out','tasks','is_billable', 'status']
    template_name = 'timesheet_form.html'
    success_message = "timesheet was updated successfully"
    success_url = reverse_lazy('list_timesheets')


class DeleteTimesheetView(DeleteView):
    """
    Delete existing timesheet
    """
    model = Timesheet
    template_name = 'timesheet_confirm_delete.html'
    success_url = reverse_lazy('list_timesheets')
