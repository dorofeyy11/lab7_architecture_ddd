class FakePaymentGateway:
    def __init__(self):
        self.charges = []

    def charge(self, order_id, money):
        self.charges.append({
            "order_id": order_id,
            "amount": money.amount,
            "currency": money.currency,
        })
