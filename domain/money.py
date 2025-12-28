class Money:
    def __init__(self, amount: int, currency: str = "USD"):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def _check_currency(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency
