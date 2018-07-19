from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers

from tracker.models import *


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff')

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    """
    Address Serializer
    """

    class Meta:
        model = Address
        fields = ('line1', 'line2', 'city_or_village', 'state', 'country', 'zip_code')


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Employee Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'employee_id', 'birth_date', 'gender', 'joined_date', 'mobile',\
                  'email', 'skype_id', 'department', 'designation', 'employment_type', 'current_pay_rate_type',\
                  'current_pay_rate', 'passport_no', 'current_visa_status', 'status', 'address')

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        emp = Employee.objects.create(**validated_data)
        emp.address = Address.objects.create(**address_data)
        emp.save()
        return emp

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.joined_date = validated_data.get('joined_date', instance.joined_date)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.skype_id = validated_data.get('skype_id', instance.skype_id)
        instance.department = validated_data.get('department', instance.department)
        instance.designation = validated_data.get('designation', instance.designation)
        instance.employment_type = validated_data.get('employment_type', instance.employment_type)
        instance.current_pay_rate_type = validated_data.get('current_pay_rate_type', instance.current_pay_rate_type)
        instance.current_pay_rate = validated_data.get('current_pay_rate', instance.current_pay_rate)
        instance.passport_no = validated_data.get('passport_no', instance.passport_no)
        instance.current_visa_status = validated_data.get('current_visa_status', instance.current_visa_status)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        address_data = validated_data.pop('address')
        address = instance.address
        address.line1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        address.city_or_village = address_data.get('city_or_village', address.city_or_village)
        address.state = address_data.get('state', address.state)
        address.country = address_data.get('country', address.country)
        address.zip_code = address_data.get('zip_code', address.zip_code)
        address.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):
    """
    Client Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'gender', 'mobile', 'email', 'skype_id', 'status', 'address')

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        client = Client.objects.create(**validated_data)
        client.address = Address.objects.create(**address_data)
        client.save()
        return client

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.skype_id = validated_data.get('skype_id', instance.skype_id)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        address_data = validated_data.pop('address')
        address = instance.address
        address.line1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        address.city_or_village = address_data.get('city_or_village', address.city_or_village)
        address.state = address_data.get('state', address.state)
        address.country = address_data.get('country', address.country)
        address.zip_code = address_data.get('zip_code', address.zip_code)
        address.save()
        return instance
