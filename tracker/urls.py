from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tracker.views import *
from tracker.utils import *


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('employees/', ListEmployeesView.as_view(), name='list_employees'),
    path('employee/add/', CreateEmployeeView.as_view(), name='add_employee'),
    path('employee/upload/', UploadEmployeeDocView.as_view(), name='upload_emp_doc'),
    path('employee/getdocs/', GetEmployeeDocuments.as_view(), name='get_emp_docs'),
    path('employee/delete_doc/<int:pk>/', DeleteEmployeeDocument.as_view(), name='delete_emp_doc'),
    path('employee/<int:pk>/edit/', UpdateEmployeeView.as_view(), name='update_employee'),
    path('employee/<int:pk>/delete/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('employees/download/', export_emps_xls, name='download_emps'),

    path('employee/<int:emp_id>/expenses/', ListEmpExpensesView.as_view(), name='list_emp_expenses'),
    path('employee/<int:emp_id>/expense/add/', CreateEmpExpenseView.as_view(), name='add_emp_expense'),
    path('employee/<int:emp_id>/expense/<int:expense_id>/edit/', UpdateEmpExpenseView.as_view(), name='update_emp_expense'),
    path('employee/<int:emp_id>/expense/<int:expense_id>/delete/', DeleteEmpExpenseView.as_view(), name='delete_emp_expense'),

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
    path('project/upload/', UploadProjectDocView.as_view(), name='upload_project_doc'),
    path('project/getdocs/', GetProjectDocuments.as_view(), name='get_project_docs'),
    path('project/delete_doc/<int:pk>/', DeleteProjectDocument.as_view(), name='delete_project_doc'),
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
    path('vendor/upload/', UploadVendorDocView.as_view(), name='upload_vendor_doc'),
    path('vendor/getdocs/', GetVendorDocuments.as_view(), name='get_vendor_docs'),
    path('vendor/delete_doc/<int:pk>/', DeleteVendorDocument.as_view(), name='delete_vendor_doc'),
    path('vendor/<int:pk>/edit/', UpdateVendorView.as_view(), name='update_vendor'),
    path('vendor/<int:pk>/delete/', DeleteVendorView.as_view(), name='delete_vendor'),

    path('vendor/<int:vendor_id>/expenses/', ListVendorExpensesView.as_view(), name='list_vendor_expenses'),
    path('vendor/<int:vendor_id>/expense/add/', CreateVendorExpenseView.as_view(), name='add_vendor_expense'),
    path('vendor/<int:vendor_id>/expense/<int:expense_id>/edit/', UpdateVendorExpenseView.as_view(),
       name='update_vendor_expense'),
    path('vendor/<int:vendor_id>/expense/<int:expense_id>/delete/', DeleteVendorExpenseView.as_view(),
       name='delete_vendor_expense'),

    path('referrals/', ListReferralsView.as_view(), name='list_referrals'),
    path('referral/add/', CreateReferralView.as_view(), name='add_referral'),
    path('referral/<int:pk>/edit/', UpdateReferralView.as_view(), name='update_referral'),
    path('referral/<int:pk>/delete/', DeleteReferralView.as_view(), name='delete_referral'),

    path('search/', ReportView.as_view(), name='report'),
    path('search/defaulters/', SearchDefaulterView.as_view(), name='get_defaulters'),

    path('gettenants/', GetTenants.as_view(), name='get_tenants'),

    path('messages/', InboxMessagesView.as_view(), name='inbox_messages'),
    path('message/add/', CreateMessageView.as_view(), name='create_message'),
    path('message/<int:pk>/edit/', UpdateMessageView.as_view(), name='update_message'),
    path('message/<int:pk>/delete/', DeleteMessageView.as_view(), name='delete_message'),

   path('tasks/', ListTasksView.as_view(), name='list_tasks'),
   path('task/add/', CreateTaskView.as_view(), name='add_task'),
   path('task/<int:pk>/edit/', UpdateTaskView.as_view(), name='update_task'),
   path('task/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)