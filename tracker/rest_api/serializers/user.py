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


class TaxInfoSerializer(serializers.ModelSerializer):
    """
    TaxInfo Serializer
    """

    class Meta:
        model = TaxInfo
        fields = ('filling_status', 'withholding_allowance', 'additional_withholding', 'is_withholding_declare')


class BankAccountInfoSerializer(serializers.ModelSerializer):
    """
    BankAccountInfo Serializer
    """

    class Meta:
        model = BankAccountInfo
        fields = ('bank_name', 'bank_routing_no', 'account_no', 'account_type')


class EmergencyContactSerializer(serializers.ModelSerializer):
    """
    EmergencyContact Serializer
    """

    class Meta:
        model = EmergencyContact
        fields = ('first_name', 'last_name', 'relation', 'mobile')


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Employee Serializer
    """
    address = AddressSerializer()
    emergency_contact = EmergencyContactSerializer()
    bank_account_info = BankAccountInfoSerializer()
    tax_info = TaxInfoSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'employee_id', 'birth_date', 'gender', 'joined_date', 'mobile',\
                  'email', 'skype_id', 'department', 'designation', 'employment_type', 'current_pay_rate_type',\
                  'current_pay_rate', 'passport_no', 'current_visa_status', 'referral_bonus_points','status', 'document',\
                  'address', 'emergency_contact', 'bank_account_info', 'tax_info', 'created_at')
        read_only_fields = ('id', 'referral_bonus_points', 'created_at',)

    @transaction.atomic
    def create(self, validated_data):
        # import pdb; pdb.set_trace()
        address_data = validated_data.pop('address')
        emergency_contact_data = validated_data.pop('emergency_contact')
        bank_acc_data = validated_data.pop('bank_account_info')
        tax_data = validated_data.pop('tax_info')
        emp = Employee.objects.create(**validated_data)
        emp.address = Address.objects.create(**address_data)
        emp.emergency_contact = EmergencyContact.objects.create(**emergency_contact_data)
        emp.bank_account_info = BankAccountInfo.objects.create(**bank_acc_data)
        emp.tax_info = TaxInfo.objects.create(**tax_data)
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
        instance.document = validated_data.get('document', instance.document)
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
        emergency_contact_data = validated_data.pop('emergency_contact')
        emergency_contact = instance.emergency_contact
        emergency_contact.first_name = emergency_contact_data.get('first_name', emergency_contact.first_name)
        emergency_contact.last_name = emergency_contact_data.get('last_name', emergency_contact.last_name)
        emergency_contact.relation = emergency_contact_data.get('relation', emergency_contact.relation)
        emergency_contact.mobile = emergency_contact_data.get('mobile', emergency_contact.mobile)
        emergency_contact.save()
        bank_account_info_data = validated_data.pop('bank_account_info')
        bank_account_info = instance.bank_account_info
        bank_account_info.bank_name = bank_account_info_data.get('bank_name', bank_account_info.bank_name)
        bank_account_info.bank_routing_no = bank_account_info_data.get('bank_routing_no', bank_account_info.bank_routing_no)
        bank_account_info.account_no = bank_account_info_data.get('account_no', bank_account_info.account_no)
        bank_account_info.account_type = bank_account_info_data.get('account_type', bank_account_info.account_type)
        bank_account_info.save()
        tax_info_data = validated_data.pop('tax_info')
        tax_info = instance.tax_info
        tax_info.filling_status = tax_info_data.get('filling_status', tax_info.filling_status)
        tax_info.withholding_allowance = tax_info_data.get('withholding_allowance', tax_info.withholding_allowance)
        tax_info.additional_withholding = tax_info_data.get('additional_withholding', tax_info.additional_withholding)
        tax_info.is_withholding_declare = tax_info_data.get('is_withholding_declare', tax_info.is_withholding_declare)
        tax_info.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):
    """
    Client Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'gender', 'mobile', 'email', 'skype_id', 'document',\
                  'status', 'address', 'created_at')
        read_only_fields = ('id', 'created_at',)

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
        instance.document = validated_data.get('document', instance.document)
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


class VendorSerializer(serializers.ModelSerializer):
    """
    Vendor Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = Vendor
        fields = ('id', 'organization_name', 'contact_person_name', 'designation', 'mobile', 'email', 'remark', 'document',\
                  'status', 'address', 'created_at')
        read_only_fields = ('id', 'created_at',)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        vendor = Vendor.objects.create(**validated_data)
        vendor.address = Address.objects.create(**address_data)
        vendor.save()
        return vendor

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.organization_name = validated_data.get('organization_name', instance.organization_name)
        instance.contact_person_name = validated_data.get('contact_person_name', instance.contact_person_name)
        instance.designation = validated_data.get('designation', instance.designation)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.status = validated_data.get('status', instance.status)
        instance.document = validated_data.get('document', instance.document)
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


class ReferralSerializer(serializers.ModelSerializer):
    """
    Referral Serializer
    """
    address = AddressSerializer()
    emp = serializers.SlugRelatedField(slug_field='email', queryset=Employee.objects.exclude(status='Delete'), \
                                       allow_null=True)

    class Meta:
        model = Referral
        fields = ('id', 'first_name', 'last_name', 'mobile', 'email', 'document', 'emp',\
                  'status', 'address', 'created_at')
        read_only_fields = ('id', 'created_at',)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        referral = Referral.objects.create(**validated_data)
        referral.address = Address.objects.create(**address_data)
        referral.save()
        return referral

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.status = validated_data.get('status', instance.status)
        instance.document = validated_data.get('document', instance.document)
        instance.emp = validated_data.get('emp', instance.emp)
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
