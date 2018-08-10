from django.contrib import admin
from django.urls import path, include

from tracker.views import *
from tracker.utils import *


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('employees/', ListEmployeesView.as_view(), name='list_employees'),
    path('employee/add/', CreateEmployeeView.as_view(), name='add_employee'),
    path('employee/<int:pk>/edit/', UpdateEmployeeView.as_view(), name='update_employee'),
    path('employee/<int:pk>/delete/', DeleteEmployeeView.as_view(), name='delete_employee'),

    path('clients/', ListClientsView.as_view(), name='list_clients'),
    path('client/add/', CreateClientView.as_view(), name='add_client'),
    path('client/<int:pk>/edit/', UpdateClientView.as_view(), name='update_client'),
    path('client/<int:pk>/delete/', DeleteClientView.as_view(), name='delete_client'),

    path('users/', ListUsersView.as_view(), name='list_users'),
    path('user/add/', CreateUserView.as_view(), name='add_user'),
    path('user/<int:pk>/edit/', UpdateUserView.as_view(), name='update_user'),
    path('user/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

    path('projects/', ListProjectsView.as_view(), name='list_projects'),
    path('project/add/', CreateProjectView.as_view(), name='add_project'),
    path('project/<int:pk>/edit/', UpdateProjectView.as_view(), name='update_project'),
    path('project/<int:pk>/delete/', DeleteProjectView.as_view(), name='delete_project'),

    path('getcontracts/', GetContractsView.as_view(), name='get_contracts'),
    path('contracts/', ListContractsView.as_view(), name='list_contracts'),
    path('contract/add/', CreateContractView.as_view(), name='add_contract'),
    path('contract/<int:pk>/edit/', UpdateContractView.as_view(), name='update_contract'),
    path('contract/<int:pk>/delete/', DeleteContractView.as_view(), name='delete_contract'),

    path('timesheets/', ListTimesheetsView.as_view(), name='list_timesheets'),
    path('timesheet/add/', CreateTimesheetView.as_view(), name='add_timesheet'),
    path('timesheet/<int:pk>/edit/', UpdateTimesheetView.as_view(), name='update_timesheet'),
    path('timesheet/<int:pk>/delete/', DeleteTimesheetView.as_view(), name='delete_timesheet'),

    path('generictimesheet/add/', GenericTimesheetView.as_view(), name='add_generic_timesheet'),

    path('tasks/', ListTasksView.as_view(), name='list_tasks'),
    path('task/add/', CreateTaskView.as_view(), name='add_task'),
    path('task/<int:pk>/edit/', UpdateTaskView.as_view(), name='update_task'),
    path('task/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
]