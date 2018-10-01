from django.urls import path, include

from rest_framework import routers

from tracker.rest_api.views.user import *
from tracker.rest_api.views.project import *

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'project_activities', ProjectActivitySet)
router.register(r'projects', ProjectViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'timesheets', TimesheetViewSet)
router.register(r'tasks', TimesheetTaskViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'referrals', ReferralViewSet)
#router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api/employees/<int:emp_id>/projects', ListProjectsOfEmployee.as_view()),
    # path('api/employees/<int:emp_id>/timesheets', ListTimesheetsOfEmployee.as_view()),
    # path('api/projects/<int:project_id>/employees', ListEmployeesOfProject.as_view()),
    # path('api/projects/<int:project_id>/timesheets', ListTimesheetsOfProject.as_view()),
    path('report', ReportView.as_view(), name='report_api'),
    path('search_defaulter', GetDefaultersView.as_view(), name='search_defaulter'),
    ]
