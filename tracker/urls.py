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

    path('getcontracts/', GetContracts.as_view(), name='get_contracts'),
    path('contracts/', ListContractsView.as_view(), name='list_contracts'),
    path('contract/add/', CreateContractView.as_view(), name='add_contract'),
    path('contract/<int:pk>/edit/', UpdateContractView.as_view(), name='update_contract'),
    path('contract/<int:pk>/delete/', DeleteContractView.as_view(), name='delete_contract'),

    path('timesheets/', ListTimesheetsView.as_view(), name='list_timesheets'),
    path('timesheet/add/', CreateTimesheetView.as_view(), name='add_timesheet'),
    path('timesheet/<int:pk>/edit/', UpdateTimesheetView.as_view(), name='update_timesheet'),
    path('timesheet/<int:pk>/delete/', DeleteTimesheetView.as_view(), name='delete_timesheet'),

    path('generictimesheet/add/', GenericTimesheetView.as_view(), name='add_generic_timesheet'),

    path('assignments/', ListAssignmentsView.as_view(), name='list_assignments'),
    path('assignment/add/', CreateAssignmentView.as_view(), name='add_assignment'),
    path('assignment/<int:pk>/edit/', UpdateAssignmentView.as_view(), name='update_assignment'),
    path('assignment/<int:pk>/delete/', DeleteAssignmentView.as_view(), name='delete_assignment'),

    path('vendors/', ListVendorsView.as_view(), name='list_vendors'),
    path('vendor/add/', CreateVendorView.as_view(), name='add_vendor'),
    path('vendor/<int:pk>/edit/', UpdateVendorView.as_view(), name='update_vendor'),
    path('vendor/<int:pk>/delete/', DeleteVendorView.as_view(), name='delete_vendor'),

    path('referrals/', ListReferralsView.as_view(), name='list_referrals'),
    path('referral/add/', CreateReferralView.as_view(), name='add_referral'),
    path('referral/<int:pk>/edit/', UpdateReferralView.as_view(), name='update_referral'),
    path('referral/<int:pk>/delete/', DeleteReferralView.as_view(), name='delete_referral'),

    path('search/', ReportView.as_view(), name='report'),
    path('search/defaulters/', SearchDefaulterView.as_view(), name='get_defaulters'),

    path('gettenants/', GetTenants.as_view(), name='get_tenants'),
]