from datetime import datetime, timedelta, time

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from tracker.models import *


class Command(BaseCommand):
    help = "Sends a notification email to defaulters of a timesheet."

    def handle(self, *args, **kwargs):
        today = datetime.today().date()
        day = today - timedelta(settings.DEFAULTER_NOTIFICATION_DAY_COUNT)
        contract_ids= Timesheet.objects.filter(sign_in__gte=datetime.combine(day, time())).\
                filter(sign_in__lte=datetime.combine(day+timedelta(1), time())).exclude(status='Delete').\
                                                                                      values_list('contract',flat=False)
        contracts = Contract.objects.filter(start_date__lte=day, status='In progress').exclude(id__in=contract_ids)
        for contract in contracts:
            if contract.employee.status == 'Available':
                send_mail(
                    'Submit Timesheet of %s For dated %s' % (contract.client.full_name, day),
                    "Hi,\nPlease, submit your timesheet.\nIf you already submitted and you got this mail, then contact your manager.\nRegards,\nTMS.",
                    settings.EMAIL_HOST_USER,
                    [contract.employee.email],
                    fail_silently=False,
                )
