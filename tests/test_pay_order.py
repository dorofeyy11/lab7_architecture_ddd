import pytest

from domain.order import Order
from domain.order_line import OrderLine
from domain.money import Money
from domain.order_status import OrderStatus

from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def create_order_with_items(order_id=1):
    order = Order(order_id)
    order.add_line(OrderLine("Product A", Money(100), 2))
    return order


def test_successful_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_order_with_items()
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)
    result = use_case.execute(order.order_id)

    assert result["status"] == OrderStatus.PAID.value
    assert result["total"] == 200
    assert len(gateway.charges) == 1


def test_cannot_pay_empty_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = Order(1)
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)

    with pytest.raises(ValueError):
        use_case.execute(order.order_id)


def test_cannot_pay_twice():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_order_with_items()
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)
    use_case.execute(order.order_id)

    with pytest.raises(ValueError):
        use_case.execute(order.order_id)


def test_cannot_modify_paid_order():
    order = create_order_with_items()
    order.pay()

    with pytest.raises(ValueError):
        order.add_line(OrderLine("Extra", Money(50), 1))


def test_total_amount_calculation():
    order = Order(1)
    order.add_line(OrderLine("A", Money(50), 2))
    order.add_line(OrderLine("B", Money(30), 1))

    total = order.total_amount()
    assert total.amount == 130
