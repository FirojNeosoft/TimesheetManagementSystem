from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from tracker.models import *


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
    fields = ['first_name', 'last_name', 'gender', 'address', 'mobile', 'email', 'skype_id', 'status']
    template_name = 'client_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_clients')


class UpdateClientView(SuccessMessageMixin, UpdateView):
    """
    Update existing client
    """
    model = Client
    fields = ['first_name', 'last_name', 'gender', 'address', 'mobile', 'email', 'skype_id', 'status']
    template_name = 'client_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_clients')


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
    fields = ['username', 'email', 'password', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was created successfully"
    success_url = reverse_lazy('list_users')


class UpdateUserView(SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """
    model = User
    fields = ['username', 'email', 'password', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was updated successfully"
    success_url = reverse_lazy('list_users')


class DeleteUserView(DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('list_users')