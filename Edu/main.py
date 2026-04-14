class main:
    def __init__(self):
        self.eventID = 0
        self.contracts = {}
        self.accounts = {}

    def place_order(self, )

    def settle_contract(self, contract_ID, settlement_value):
        try:
            contract_ID = int(contract_ID)
            settlement_value = int(settlement_value)
        except:
            return False, "Input Conversion Error"
        if contract_ID not in self.contracts:
            return False, "The specified Contract does not exist"
        if (
            settlement_value < 1
            or settlement_value > self.contracts[contract_ID].max_settlement
        ):
            return False, "The requested settlement value is illegal"

        contract = self.contracts[contract_ID]
        for side_book in contract.book:
            for order in side_book:
                contract.remove_order(order, ignore_book=True)

        for account in self.accounts:
            acct_positions = account.positions
            if contract_id in acct_positions:
                acct_positions[contract_ID].settle_contract
