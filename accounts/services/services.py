"""
Accounts Services
"""

from accounts.models import GeneralLedger
from decimal import Decimal



class CoreAccountServices:
    """
    Core account services like account group creation and accounts
    """

    def __init__(self, branch, company, user):
        self.branch = branch
        self.company = company
        self.user = user


    def create_ledger(
            self,
            *,
            gl_id,
            voucher_no,
            voucher_type,
            account,
            against_account,
            account_currency,
            transaction_currency,
            debit_amount_ac=Decimal("0.00"),
            credit_amount_ac=Decimal("0.00"),
            debit_amount_tc=Decimal("0.00"),
            credit_amount_tc=Decimal("0.00"),
            debit_amount=Decimal("0.00"),
            credit_amount=Decimal("0.00"),
            transaction_exchange_rate=Decimal("1.000000"),
            account_exchange_rate=Decimal("1.000000"),
            posting_date=None,
            customer=None,
            supplier=None,
            party_type=None,
            voucher_sub_type=None,
            against_voucher=None,
            against_voucher_type=None,
            fiscal_year=None,
            fiscal_period=None,
            remarks=None,
    ):
        """
        Create Ledger
        """

        ledger = GeneralLedger.objects.create(
            gl_id=gl_id,
            voucher_no=voucher_no,

            debit_amount_ac=debit_amount_ac,
            credit_amount_ac=credit_amount_ac,
            account_currency=account_currency,

            debit_amount_tc=debit_amount_tc,
            credit_amount_tc=credit_amount_tc,
            transaction_currency=transaction_currency,

            debit_amount=debit_amount,
            credit_amount=credit_amount,

            transaction_exchange_rate=transaction_exchange_rate,
            account_exchange_rate=account_exchange_rate,

            posting_date=posting_date,

            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,

            customer=customer,
            supplier=supplier,

            account=account,
            against_account=against_account,

            company=self.company,
            branch=self.branch,

            party_type=party_type,

            voucher_type=voucher_type,
            voucher_sub_type=voucher_sub_type,

            against_voucher=against_voucher,
            against_voucher_type=against_voucher_type,

            remarks=remarks,

            created_by=self.user
        )

        return ledger


    def validate_amounts(self, debit_amount, credit_amount):

        debit_amount = Decimal(debit_amount)
        credit_amount = Decimal(credit_amount)

        if debit_amount < 0 or credit_amount < 0:
            raise ValueError(
                "Debit and credit amounts cannot be negative."
            )

        if debit_amount > 0 and credit_amount > 0:
            raise ValueError(
                "A ledger entry cannot have both debit and credit."
            )

        if debit_amount == 0 and credit_amount == 0:
            raise ValueError(
                "Either debit or credit amount must be greater than zero."
            )


            


