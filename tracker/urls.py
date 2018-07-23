from django.contrib import admin
from django.urls import path, include

from tracker.views import *


urlpatterns = [
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
]