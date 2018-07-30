from django.http import JsonResponse
from django.views.generic import View

from tracker.models import *


class GetContractsView(View):
    """
       Get all contracts
    """

    def get(self, request):
        """
        Get all contracts
        """

        contracts = Contract.objects.exclude(status='delete')

        contract_list = []
        for contract in contracts:
            contract_list.append({'id': contract.id,
                                 'name': contract.__str__()})
        return JsonResponse({'contract_list': contract_list})
