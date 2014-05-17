from django.db.models import Q
from customer.models import RealCustomerInformation
from start_grant.models import CheckList, CheckListItem, CheckListItemInstance


def createCheckList(request):
    if hasattr(request,'check_list'):
        request.check_list.delete()
    if request.type == 'haghighi':
        return RealCustomerCheckListGenerator(request).createCheckList()


class RealCustomerCheckListGenerator:
    def __init__(self, request):
        if request.type != 'haghighi':
            raise Exception('request shoud be real but is %s' % request.type)

        self.customer = RealCustomerInformation.objects.get(customer_code=request.cif)
        self.request = request


    def createCheckList(self):
        checklist = CheckList()
        checklist.request_id = self.request.id
        checklist.save()
        checklist_items = set()

        self._createCustomerInfoCheckList(checklist_items)
        self._createContactInfoCheckList(checklist_items)
        self._createJobInfoCheckList(checklist_items)
        self._createLoanInfoCheckList(checklist_items)
        self._createAssetCheckList(checklist_items)
        self._createBankInfoCheckList(checklist_items)

        for item in checklist_items:
            chitem = CheckListItemInstance()
            chitem.item_id = item
            chitem.checklist = checklist
            chitem.save()


    def _createCustomerInfoCheckList(self, source):
        source.add(1)
        source.add(2)

    def _createContactInfoCheckList(self, source):
        source.add(3)

    def _createJobInfoCheckList(self, source):
        source.add(4)
        source.add(5)

    def _createLoanInfoCheckList(self, source):
        source.add(6)


    def _createAssetCheckList(self, source):
        asset = self.customer.asset_info
        source.add(7)

        if asset.account != 0:
            source.add(6)

        if asset.individual_credit_amount != 0:
            source.add(8)

        if asset.company_credit_amount != 0:
            source.add(9)

        if asset.manghool_value != 0:
            source.add(10)

        if asset.no_manghool_value != 0:
            source.add(11)

        if asset.vehicles_value != 0:
            source.add(12)

        if asset.individual_debit_amount != 0:
            source.add(13)

        if asset.company_debit_amount != 0:
            source.add(14)

        if asset.bank_debit_amount != 0:
            source.add(15)

    def _createBankInfoCheckList(self, source):
        source.add(16)
        source.add(17)

        if self.request.need_guarantor():
            source.add(19)

        if self.request.vasighe_information.vasighe_types.exclude(Q(id=2) | Q(id=3)).exists():
            source.add(18)







