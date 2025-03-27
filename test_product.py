import pytest
from products import Product


def test_create_product_successfully():
    """
    Test that a product is successfully created when provided with valid input values.
    The test ensures that the product has the correct name, price, and quantity after creation.
    :return: None
    """

    product = Product(name="MacBook Air M2", price=1450.0, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450.0
    assert product.quantity == 100
    assert product.is_active() == True

def test_create_invalid_product():
    """
    Test that creating a product with invalid input values (e.g. empty name or negative price)
    raises a ValueError exception.
    :return: None
    """

    # Empty name
    with pytest.raises(ValueError):
        Product(name="", price=1450.0, quantity=100)

    # Negative price
    with pytest.raises(ValueError):
        Product(name="MacBook Air M2", price=-1450.0, quantity=100)

def test_product_status():
    """
    Test that when the quantity of a product is set to 0, it becomes inactive.
    The test ensures that the 'active' status of the product is set to False after the quantity is reduced to 0.
    :return: None
    """

    product = Product(name="MacBook Air M2", price=1450.0, quantity=100)
    product.set_quantity(0)

    assert product.is_active() == False

def test_product_quantity_and_total_price():
    """
    Test that the quantity of a product is correctly modified after a purchase
    and that the total price returned is accurate. This ensures that the system
    correctly handles product purchases by updating the inventory and calculating
    the correct total price based on the quantity purchased.
    :return: None
    """

    product = Product(name="MacBook Air M2", price=1450.0, quantity=100)

    total_price = product.buy(50)

    assert product.quantity == 50
    assert total_price == product.price * 50

def test_buying_more_than_available():
    """
    Test that when a user tries to purchase more products than are available in stock,
    a ValueError exception is raised. This ensures that the system properly handles
    out-of-stock scenarios and prevents purchasing more items than are in inventory.
    :return: None
    """

    product = Product(name="MacBook Air M2", price=1450.0, quantity=100)

    with pytest.raises(ValueError):
        product.buy(200)