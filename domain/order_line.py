from domain.money import Money


class OrderLine:
    def __init__(self, product_name: str, price: Money, qty: int):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        self.product_name = product_name
        self.price = price
        self.qty = qty

    def total_price(self) -> Money:
        return Money(self.price.amount * self.qty, self.price.currency)
