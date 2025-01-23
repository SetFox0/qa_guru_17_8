"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def product_2():
    return Product("pencil", 20, "This is a pencil", 20)

@pytest.fixture
def cart(product):
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        initial_quantity = product.quantity
        product.buy(100)
        assert product.quantity == initial_quantity - 100

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match="Not enough book") as exc_info:
            product.buy(1500)
        assert str(exc_info.value) == "Not enough book"


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        cart.add_product(product, 2)
        assert cart.products[product] == 2

        cart.add_product(product, 3)
        assert cart.products[product] == 5

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)

        cart.remove_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product_more_than_quantity(self, cart, product):
        cart.add_product(product, 4)
        cart.remove_product(product, 5)
        assert product not in cart.products

    def test_remove_product_without_quantity(self, cart, product):
        cart.add_product(product, 4)
        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, cart, product, product_2):
        cart.add_product(product, 2)
        cart.add_product(product_2, 3)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product, product_2):
        cart.add_product(product, 2)
        cart.add_product(product_2, 3)
        assert cart.get_total_price() == 260

    def test_buy_success(self, cart, product, product_2):
        cart.add_product(product, 5)
        cart.add_product(product_2, 10)

        initial_quantity_product = product.quantity
        initial_quantity_product_2 = product_2.quantity

        cart.buy()

        assert product.quantity == initial_quantity_product - 5
        assert product_2.quantity == initial_quantity_product_2 - 10
        assert len(cart.products) == 0

    def test_buy_insufficient_quantity(self, cart, product):
        cart.add_product(product, 1500)

        with pytest.raises(ValueError, match="Not enough book") as exc_info:
            cart.buy()
        assert str(exc_info.value) == "Not enough book"
