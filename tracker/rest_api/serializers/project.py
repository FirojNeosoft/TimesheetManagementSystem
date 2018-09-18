from django.db import transaction

from rest_framework import serializers

from tracker.models import *
from tracker.rest_api.serializers.user import *


class ProjectActivitySerializer(serializers.ModelSerializer):
    """
    ProjectActivity Serializer
    """

    class Meta:
        model = ProjectActivity
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    """
    Project Serializer
    """

    owner = serializers.SlugRelatedField(slug_field='email', queryset=Client.objects.all())
    project_members = serializers.SlugRelatedField(slug_field='email', many=True, queryset=Employee.objects.all())
    project_activities = serializers.SlugRelatedField(slug_field='name', many=True, queryset=ProjectActivity.objects.all())
    located_at = AddressSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'project_members', 'project_activities', 'status', 'located_at', 'owner', 'document', 'created_at')
        read_only_fields = ('id', 'created_at',)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('located_at')
        team_members = validated_data.pop('project_members')
        tasks = validated_data.pop('project_activities')
        project = Project.objects.create(**validated_data)
        project.located_at = Address.objects.create(**address_data)
        if team_members:
            for member in team_members:
                project.project_members.add(member)
        if tasks:
            for task in tasks:
                project.project_activities.add(task)
        project.save()
        return project

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.document = validated_data.get('document', instance.document)

        team_members = validated_data.pop('project_members')
        tasks = validated_data.pop('project_activities')
        if team_members:
            instance.project_members.clear()
            for member in team_members:
                instance.project_members.add(member)
        if tasks:
            instance.project_activities.clear()
            for task in tasks:
                instance.project_activities.add(task)
        instance.save()
        address_data = validated_data.pop('located_at')
        address = instance.located_at
        address.line1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        address.city_or_village = address_data.get('city_or_village', address.city_or_village)
        address.state = address_data.get('state', address.state)
        address.country = address_data.get('country', address.country)
        address.zip_code = address_data.get('zip_code', address.zip_code)
        address.save()
        return instance


class ContractSerializer(serializers.ModelSerializer):
    """
    Contract Serializer
    """

    employee = serializers.SlugRelatedField(slug_field='email', queryset=Employee.objects.exclude(designation='Sales Executive'))
    representative = serializers.SlugRelatedField(slug_field='email',
                                            queryset=Employee.objects.exclude(status='Delete'))
    client = serializers.SlugRelatedField(slug_field='email',
                                            queryset=Client.objects.exclude(status='Delete'))
    referral = serializers.SlugRelatedField(slug_field='email', queryset=Referral.objects.exclude(status='Delete'))

    class Meta:
        model = Contract
        fields = ('id', 'representative', 'client', 'employee', 'role', 'start_date', 'end_date', 'duration_per_day', 'pay_rate_type',\
                  'pay_rate', 'billing_cycle', 'remark', 'document', 'referral', 'status', 'created_at')
        read_only_fields = ('id', 'created_at',)


class TimesheetSerializer(serializers.ModelSerializer):
    """
    Timesheet Serializer
    """

    contract = serializers.SlugRelatedField(slug_field='id', queryset=Contract.objects.exclude(status='Delete'))

    class Meta:
        model = Timesheet
        fields = ('id', 'contract', 'sign_in', 'sign_out', 'document', 'remark', 'status', 'created_at')
        read_only_fields = ('id', 'created_at', 'status',)


class TimesheetTaskSerializer(serializers.ModelSerializer):
    """
    TimesheetTask Serializer
    """

    timesheet = serializers.SlugRelatedField(slug_field='id', queryset=Timesheet.objects.exclude(status='Delete'))
    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.exclude(status='Delete'))
    activity = serializers.SlugRelatedField(slug_field='name', queryset=ProjectActivity.objects.all())

    class Meta:
        model = TimesheetTask
        fields = ('id', 'timesheet', 'start_time', 'end_time', 'project', 'activity', 'note', 'is_billable', 'created_at')
        read_only_fields = ('id', 'created_at',)


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Assignment Serializer
    """

    emp = serializers.SlugRelatedField(slug_field='email', queryset=Employee.objects.exclude(status='Delete'), \
                                       allow_null=True)
    activity = serializers.SlugRelatedField(slug_field='name', queryset=ProjectActivity.objects.all())


    class Meta:
        model = Assignment
        fields = ('id', 'emp', 'due_date', 'activity', 'note', 'document', 'status', 'created_at')
        read_only_fields = ('id', 'created_at', 'status',)


class InvoiceItemSerializer(serializers.ModelSerializer):
    """
    InvoiceItem Serializer
    """

    class Meta:
        model = InvoiceItem
        fields = ('service_name', 'pay_rate', 'quantity')


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Invoice Serializer
    """

    client = serializers.SlugRelatedField(slug_field='email', queryset=Client.objects.all())
    services = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ('id', 'client', 'due_date', 'services', 'total_amount', 'tax', 'discount', 'remark', 'document',\
                  'status', 'created_at')
        read_only_fields = ('id', 'created_at',)

    @transaction.atomic
    def create(self, validated_data):
        services = validated_data.pop('services')
        invoice = Invoice.objects.create(**validated_data)
        for service in services:
            invoice.services.add(InvoiceItem.objects.create(service_name=service['service_name'],\
                                                             pay_rate=service['pay_rate'], quantity=service['quantity']))
        return invoice

    @transaction.atomic
    def update(self, instance, validated_data):
        services = validated_data.pop('services')
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.status = validated_data.get('status', instance.status)
        instance.client = validated_data.get('client', instance.client)
        instance.document = validated_data.get('document', instance.document)
        instance.save()
        instance.services.clear()
        for service in services:
            instance.services.add(InvoiceItem.objects.create(service_name=service['service_name'],\
                                                             pay_rate=service['pay_rate'], quantity=service['quantity']))
        return instance
