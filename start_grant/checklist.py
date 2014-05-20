from django.db.models import Q
from customer.models import RealCustomerInformation
from customer.models.enterprise_models import EnterpriseCustomerInformation
from start_grant.models import CheckList, CheckListItem, CheckListItemInstance


def createCheckList(request):
    if hasattr(request, 'check_list'):
        request.check_list.delete()
    if request.type == 'haghighi':
        return RealCustomerCheckListGenerator(request).createCheckList()

    if request.type == 'hoghooghi':
        return EnterpriseCustomerCheckListGeneraotr(request).createCheckList()


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


class EnterpriseCustomerCheckListGeneraotr:
    def __init__(self, request):
        if request.type != 'hoghooghi':
            raise Exception('request shoud be enterprise but is %s' % request.type)

        self.customer = EnterpriseCustomerInformation.objects.get(customer_code=request.cif)
        self.request = request

    def createCheckList(self):
        checklist = CheckList()
        checklist.request_id = self.request.id
        checklist.save()
        checklist_items = set()

        self._createCustomerInfoCheckList(checklist_items)
        self._createBoardOfDirectorCheckList(checklist_items)
        self._createContactInfoCheckList(checklist_items)
        self._createActivityInfoCheckList(checklist_items)
        self._createLoanInfoCheckList(checklist_items)
        self._createAssetInfoCheckList(checklist_items)

        for item in checklist_items:
            chitem = CheckListItemInstance()
            chitem.item_id = item
            chitem.checklist = checklist
            chitem.save()

    def _createCustomerInfoCheckList(self, source):
        source.add(101)
        source.add(102)

    def _createBoardOfDirectorCheckList(self, source):
        source.add(1)
        source.add(1)
        source.add(105)

    def _createContactInfoCheckList(self, source):
        source.add(3)


    def _createActivityInfoCheckList(self, source):
        source.add(106)

    def _createLoanInfoCheckList(self, source):
        source.add(6)

    def _createAssetInfoCheckList(self, source):
        asset = self.customer.asset_info

        if asset.account != 0:
            source.add(6)

        if asset.ingredient != 0 or asset.current_develop_products_amount != 0 or asset.current_products_amount != 0 or asset.individual_credit_amount != 0 or asset.other_credit_amount != 0 or asset.company_credit_amount != 0 or asset.manghool_installation_amount != 0 or asset.manghool_building_amount != 0 or asset.manghool_vehicle_amount != 0:
            source.add(107)

        if asset.registered_payed != 0 or asset.registered_guarantied != 0 or asset.remained_benefit_amount != 0 or asset.loan_from_individual_amount != 0 or asset.loan_from_banks_amount != 0 or asset.loan_from_institutes_amount != 0 or asset.pish_daryaft_amount != 0 or asset.bestankaran_amount != 0 or asset.payed_documents_amount != 0:
            source.add(108)











