class main:
    def __init__(self):
        self.eventID = 0
        self.contracts = {}
        self.accounts = {}

    def settle_contract(self, contract_ID):
        try:
            contract_ID = int(contract_ID)
        except:
            return False
        if contract_ID not in self.contracts:
            return False

        contract = self.contracts[contract_ID]
        for side_book in contract.book:
            for order in side_book:
                contract.remove_order(order, ignore_book=True)

        for account in self.accounts:
            acct_positions = account.positions
            if contract_id in acct_positions:
                pos
