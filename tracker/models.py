from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator

from django.db.models.signals import post_save
from django.dispatch import receiver


class Address(models.Model):
    """
    Address model
    """
    line1 = models.CharField(max_length=128, blank=True, null=True)
    line2 = models.CharField(max_length=128, blank=True, null=True)
    city_or_village = models.CharField(max_length=128, blank=False, null=False)
    state = models.CharField(max_length=128, blank=False, null=False)
    country = models.CharField(max_length=128, blank=False, null=False)
    zip_code = models.PositiveIntegerField('Zip Code', blank=False, null=False)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.country

    def delete(self):
        """
        Delete address
        """
        self.status = 'Delete'
        self.save()


class EmergencyContact(models.Model):
    """
    EmergencyContact model
    """
    first_name = models.CharField('First Name', max_length=128, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=128, blank=False, null=False)
    relation = models.CharField('Relation', max_length=32, blank=False, null=False)
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  blank=False, null=False)

    def __str__(self):
        return '%s(%s)' % (self.mobile, self.relation)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)


class BankAccountInfo(models.Model):
    """
    BankAccountInfo model
    """
    bank_name = models.CharField('Bank Name', max_length=128, blank=False, null=False)
    bank_routing_no = models.CharField('Routing No', max_length=128, blank=False, null=False)
    account_no = models.CharField('Account No', max_length=32, blank=False, null=False)
    account_type = models.CharField(max_length=10, choices=settings.BANK_ACC_TYPE)

    def __str__(self):
        return '%s(Account No- %s)' % (self.bank_name, self.account_no)


class EmpTaxInfo(models.Model):
    """
    Employee Tax Info model
    """
    filling_status = models.CharField('Filling Status', max_length=15, choices=settings.TAX_RETURN_TYPE)
    withholding_allowance = models.DecimalField('Withholding Allowance', max_digits=10, decimal_places=2, blank=False,\
                                                null=False, default=0)
    additional_withholding = models.DecimalField('Additional Withholding', max_digits=10, decimal_places=2, blank=False,\
                                                 null=False, default=0)
    is_withholding_declare = models.BooleanField('Is Withholding Declare', default=False)

    def __str__(self):
        return self.filling_status


class Employee(models.Model):
    """
    Employee model
    """
    first_name = models.CharField('First Name', max_length=128, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=128, blank=False, null=False)
    employee_id = models.CharField('Employee Id', max_length=32, blank=True, null=True)
    birth_date = models.DateField('Birth Date', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=settings.GENDER_CHOICES, blank=False, null=False)
    # photo = models.ImageField(upload_to='emp_photos/', default='emp_photos/no-photo.jpeg')
    address = models.ForeignKey('Address', related_name='employee', blank=False, null=True, on_delete=models.SET_NULL)
    joined_date = models.DateField('Joint Date', blank=True, null=True)
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False, unique=True)
    skype_id = models.CharField('skype Id', max_length=128, blank=True, null=True)
    department = models.CharField('Department', max_length=128, blank=False, null=False)
    designation = models.CharField('Designation', max_length=128, blank=False, null=False)
    employment_type = models.CharField(max_length=10, choices=settings.EMPLOYEMENT_TYPE)
    current_pay_rate_type = models.CharField(max_length=10, choices=settings.PAY_RATE_TYPE)
    current_pay_rate = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    passport_no = models.CharField('Passport No', max_length=128, blank=True, null=True)
    current_visa_status = models.CharField(max_length=12,  blank=True, null=True)
    referral_bonus_points = models.IntegerField(blank=False, null=False, default=0)
    emergency_contact = models.OneToOneField('EmergencyContact', related_name='employee', blank=False, null=True,\
                                             on_delete=models.SET_NULL)
    bank_account_info = models.OneToOneField('BankAccountInfo', related_name='employee', blank=False, null=True,\
                                             on_delete=models.SET_NULL)
    tax_info = models.OneToOneField('EmpTaxInfo', related_name='employee', blank=False, null=True,\
                                    on_delete=models.SET_NULL)
    document = models.FileField('Document', upload_to='upload_docs/employee/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=settings.EMPLOYEE_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def delete(self):
        """
        Delete employee
        """
        self.status = 'Delete'
        self.save()


class Client(models.Model):
    """
    Client model
    """
    first_name = models.CharField('First Name', max_length=128, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=128, blank=False, null=False)
    gender = models.CharField(max_length=1, choices=settings.GENDER_CHOICES, blank=False, null=False)
    # photo = models.ImageField(upload_to='emp_photos/', default='emp_photos/no-photo.jpeg')
    address = models.ForeignKey('Address', related_name='client', blank=False, null=True, on_delete=models.SET_NULL)
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False, unique=True)
    skype_id = models.CharField('skype Id', max_length=128, blank=True, null=True)
    document = models.FileField('Document', upload_to='upload_docs/client/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def delete(self):
        """
        Delete client
        """
        self.status = 'Delete'
        self.save()


class Project(models.Model):
    """
    Project model
    """
    name = models.CharField('Project Name', max_length=128, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey('Client', related_name='project', blank=False, null=True, on_delete=models.CASCADE)
    representative = models.ForeignKey('Employee', related_name='project', blank=False, null=True, on_delete=models.SET_NULL)
    located_at = models.ForeignKey('Address', related_name='project', blank=True, null=True, on_delete=models.SET_NULL)
    document = models.FileField('Document', upload_to='upload_docs/project/', null=True, blank=True)
    status = models.CharField(max_length=12, choices=settings.PROJECT_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return '%s' % self.name

    def delete(self):
        """
        Delete project
        """
        self.status = 'Delete'
        self.save()


class Contract(models.Model):
    """
    Contract model
    """
    employee = models.ForeignKey('Employee', related_name='contract', blank=False, null=False, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', related_name='contract', blank=False, null=False, on_delete=models.CASCADE)
    role = models.CharField('Role', max_length=128, blank=False, null=False)
    start_date = models.DateField('Start Date', blank=False, null=False)
    end_date = models.DateField('End Date', blank=True, null=True)
    duration_per_day = models.PositiveIntegerField('Duration Per Day', blank=False, null=False)
    pay_rate_type = models.CharField('Pay Rate Type', max_length=10, choices=settings.PAY_RATE_TYPE)
    pay_rate = models.DecimalField('Pay Rate', max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    billing_cycle = models.CharField('Billing Cycle', max_length=10, choices=settings.PAY_RATE_TYPE)
    referral = models.ForeignKey('Referral', related_name='contract', blank=True, null=True,
                            on_delete=models.SET_NULL)
    remark = models.TextField(null=True, blank=True)
    document = models.FileField('Document', upload_to='upload_docs/contract/', null=True, blank=True)
    status = models.CharField(max_length=12, choices=settings.PROJECT_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return '%s(%s)' % (self.project.name, self.employee.full_name)

    def delete(self):
        """
        Delete contract
        """
        self.status = 'Delete'
        self.save()


class Timesheet(models.Model):
    """
    Timesheet model
    """
    contract = models.ForeignKey('Contract', related_name='timesheet', blank=False, null=False, on_delete=models.CASCADE)
    sign_in = models.DateTimeField('Sign In')
    sign_out = models.DateTimeField('Sign Out')
    tasks = models.TextField(null=True, blank=True)
    is_billable = models.BooleanField('Is Billable', default=True)
    document = models.FileField('Document', upload_to='upload_docs/timesheet/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=settings.TIMESHEET_STATUS, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Timesheet"
        verbose_name_plural = "Timesheets"

    def __str__(self):
        return '%s(%s)- %s' % (self.contract.project.name, self.contract.employee.full_name, self.sign_in.date())

    def delete(self):
        """
        Delete timesheet
        """
        self.status = 'Delete'
        self.save()


class TaskAllocation(models.Model):
    """
    TaskAllocation model
    """
    emp = models.ForeignKey('Employee', related_name='task_allocation', blank=True, null=True, on_delete=models.SET_NULL)
    due_date = models.DateField('Due Date', blank=True, null=True)
    title = models.CharField('Title', max_length=64, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    document = models.FileField('Document', upload_to='upload_docs/task/', null=True, blank=True)
    status = models.CharField(max_length=15, choices=settings.PROJECT_STATUS, default='In progress')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Task Allocation"

    def __str__(self):
        return self.title

    def delete(self):
        """
        Delete task
        """
        self.status = 'Delete'
        self.save()


class InvoiceItem(models.Model):
    """
    InvoiceItem model
    """
    service_name = models.CharField(max_length=128, blank=True, null=True)
    pay_rate = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.service_name

    def delete(self):
        """
        Delete InvoiceItem
        """
        self.status = 'Delete'
        self.save()


class Invoice(models.Model):
    """
    Invoice model
    """
    client = models.ForeignKey('Client', related_name='invoice', blank=False, null=False, on_delete=models.CASCADE)
    due_date = models.DateField('Due Date', blank=False, null=False)
    services = models.ManyToManyField('InvoiceItem', related_name='invoice', blank=False)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    tax = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, default=0)
    remark = models.TextField(null=True, blank=True)
    document = models.FileField('Document', upload_to='upload_docs/invoice/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=settings.INVOICE_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id

    def delete(self):
        """
        Delete Invoice
        """
        self.status = 'Delete'
        self.save()


class Vendor(models.Model):
    """
    vendor model
    """
    organization_name = models.CharField('Organization Name', max_length=128, blank=True, null=True)
    contact_person_name = models.CharField('Name Of Contact Person', max_length=128, blank=True, null=True)
    designation = models.CharField(max_length=64, blank=True, null=True)
    address = models.ForeignKey('Address', related_name='vendor', blank=True, null=True, on_delete=models.SET_NULL)
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False, unique=True)
    remark = models.TextField(null=True, blank=True)
    document = models.FileField('Document', upload_to='upload_docs/vendor/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return '%s(%s)' % (self.organization_name, self.contact_person_name)

    def delete(self):
        """
        Delete vendor
        """
        self.status = 'Delete'
        self.save()


class Referral(models.Model):
    """
    Referral model
    """
    first_name = models.CharField('First Name', max_length=128, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=128, blank=False, null=False)
    address = models.ForeignKey('Address', related_name='referral', blank=False, null=True, on_delete=models.SET_NULL)
    mobile = models.CharField('Mobile', validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:\
                                  '+999999999'. Up to 15 digits allowed.")], max_length=15,\
                                  unique=True, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False, unique=True)
    document = models.FileField('Document', upload_to='upload_docs/referral/', null=True, blank=True)
    emp = models.ForeignKey('Employee', related_name='referral', blank=True, null=True,
                            on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=settings.STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def delete(self):
        """
        Delete referral
        """
        self.status = 'Delete'
        self.save()


@receiver(post_save, sender=Contract)
def add_referral_points(sender, instance, created, **kwargs):
    if created:
        bonus_points = instance.project.representative.referral_bonus_points
        instance.project.representative.referral_bonus_points = bonus_points+1
        instance.project.representative.save()
