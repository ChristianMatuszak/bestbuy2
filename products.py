from colorama import Fore, Style
from abc import ABC, abstractmethod


class Product:
    """
    Represents a product in an inventory system.
    Attributes:
        name (str): The name of the product.
        price (float): The price of the product (must be non-negative).
        quantity (int): The available stock quantity (must be non-negative).
        active (bool): Indicates whether the product is available for sale.
        promotion (Promotion): Optional promotion applied to the product.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a new Product instance.

        :param name: The name of the product (must be a non-empty string).
        :type name: str
        :param price: The price of the product (must be >= 0).
        :type price: float
        :param quantity: The stock quantity of the product (must be >= 0).
        :type quantity: int
        :raises ValueError: If name is empty, price is negative, or quantity is negative.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Invalid name: name should be a string")
        if not isinstance(price, (float, int)) or price < 0:
            raise ValueError("Invalid price: price should be a non-negative float")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Invalid quantity: quantity should be a non-negative integer")

        self.name = name
        self.price = float(price)
        self.quantity = quantity
        self.active = True
        self.promotion = None

    def __str__(self):
        """
        Returns a user-friendly string representation of the product.
        :return: A string that includes the product name and price
        :rtype: str
        """
        return f"{self.name} (Price: {self.price:.2f}€)"

    def get_quantity(self) -> float:
        """
        Returns the quantity of the product.
        :return: Quantity of the product.
        :rtype: int
        """
        return float(self.quantity)

    def set_quantity(self, quantity):
        """
        Updates the product quantity after validation.
        If the quantity is set to 0, the product is deactivated.
        :param quantity: The new quantity value to be set.
        :type quantity: int
        :raises ValueError: If quantity is not a non-negative integer.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Invalid input: quantity should be a non-negative integer")
        self.quantity = quantity

        if quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """
        Checks if the product is active.
        :return: True if the product is active, otherwise False.
        :rtype: bool
        """
        return self.active

    def activate(self):
        """
        Activates the product if it has more than 0 quantity.
        :return: True if the product was successfully activated, otherwise False.
        :rtype: bool
        """
        if self.quantity > 0:
            self.active = True
            return True
        return False

    def deactivate(self):
        """
        Deactivates the product.
        :return: True if the product was successfully deactivated.
        :rtype: bool
        """
        self.active = False
        return True

    def set_promotion(self, promotion):
        """
        Assigns a promotion to the product.
        :param promotion: The promotion to be applied.
        :type promotion: Promotion
        :return: None
        """
        self.promotion = promotion

    def get_promotion(self):
        """
        Returns the promotion applied to the product.
        :return: The current promotion or None if no promotion is set.
        :rtype: Promotion or None
        """
        return self.promotion

    def show(self) -> str:
        """
        Returns a formatted string with product details.
        If a promotion is applied, it includes the promotion name.
        :return: A formatted string containing the product name, price, quantity, and promotion.
        :rtype: str
        """
        promo_text = f" - Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price:.2f}, Quantity: {self.quantity}{promo_text}"

    def buy(self, quantity) -> float:
        """
        Buys a given quantity of the product if it is available.
        Calculates the total purchase price and updates the quantity.
        If a promotion is applied, it uses the promotion price.
        :param quantity: The quantity to be purchased.
        :type quantity: int
        :return: The total price of the purchase.
        :rtype: float
        :raises ValueError: If the quantity is invalid or not enough stock is available.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Invalid input: quantity should be a positive integer")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available")

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return total_price


class NonStockedProduct(Product):
    """
    Represents a product that is not stocked in the store, such as digital products or licenses.
    The quantity is always set to 0 and does not restrict purchases.
    """

    def __init__(self, name: str, price: float):
        """
        Initializes a non-stocked product with the provided name and price.
        :param name: The name of the product.
        :type name: str
        :param price: The price of the product.
        :type price: float
        """
        super().__init__(name, price, quantity=0)
        self.is_stocked = False

    def show(self) -> str:
        """
        Returns a string representation of the non-stocked product, including its name and price.
        Includes promotion name if available.
        :return: A formatted string with product details.
        :rtype: str
        """
        promo_text = f" - Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name} - Price: {self.price:.2f}€{promo_text}"

    def buy(self, quantity: int) -> float:
        """
        Buys a non-stocked product (e.g., digital license). Quantity is unrestricted.
        :param quantity: The quantity to be purchased.
        :type quantity: int
        :return: Total price of the purchase.
        :rtype: float
        :raises ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError(Fore.RED + "Invalid quantity. It must be a positive integer." + Style.RESET_ALL)
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return quantity * self.price


class LimitedProduct(Product):
    """
    Represents a product with a limit on the quantity that can be purchased per order.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initializes a limited product with a maximum purchase limit.
        :param name: The name of the product.
        :type name: str
        :param price: The price of the product.
        :type price: float
        :param quantity: Quantity in stock.
        :type quantity: int
        :param maximum: Maximum units allowed per order.
        :type maximum: int
        """
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self) -> str:
        """
        Returns a string representation of the limited product.
        Includes max per order and promotion if applicable.
        :return: A formatted string with product details.
        :rtype: str
        """
        promo_text = f" - Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name} - Price: {self.price:.2f}€ - Available: {self.quantity} - Max purchase per order: {self.maximum}{promo_text}"

    def buy(self, quantity) -> float:
        """
        Buys a given quantity of the product, respecting the maximum per order.
        :param quantity: The quantity to be purchased.
        :type quantity: int
        :return: The total price of the purchase.
        :rtype: float
        :raises ValueError: If quantity exceeds limits or is invalid.
        """
        if quantity <= 0:
            raise ValueError(Fore.RED + "Invalid quantity. It must be a positive integer." + Style.RESET_ALL)
        if quantity > self.maximum:
            raise ValueError(Fore.RED + f"Cannot purchase more than {self.maximum} units of this item." + Style.RESET_ALL)
        if quantity > self.quantity:
            raise ValueError("Not enough stock available")

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return total_price


class Promotion(ABC):
    """
    Abstract base class for promotions. Subclasses must implement the apply_promotion method.
    """

    def __init__(self, name: str):
        """
        Initializes a promotion with a name.
        :param name: The name of the promotion.
        :type name: str
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Applies the promotion to the given product and quantity.
        :param product: The product to which the promotion is applied.
        :type product: Product
        :param quantity: The quantity being purchased.
        :type quantity: int
        :return: The total discounted price.
        :rtype: float
        """
        pass


class SecondHalfPrice(Promotion):
    """
    Promotion where every second item is half price.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Applies 'second item at half price' promotion.
        :param product: The product being purchased.
        :type product: Product
        :param quantity: Quantity being purchased.
        :type quantity: int
        :return: Total discounted price.
        :rtype: float
        """
        if quantity == 1:
            return product.price
        full_price_quantity = quantity // 2
        half_price_quantity = quantity - full_price_quantity
        return (full_price_quantity * product.price) + (half_price_quantity * product.price / 2)


class ThirdOneFree(Promotion):
    """
    Promotion where every third item is free.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Applies buy 2, get 1 free promotion.
        :param product: The product being purchased.
        :type product: Product
        :param quantity: Quantity being purchased.
        :type quantity: int
        :return: Total discounted price.
        :rtype: float
        """
        free_quantity = quantity // 3
        paid_quantity = quantity - free_quantity
        return paid_quantity * product.price


class PercentDiscount(Promotion):
    """
    Promotion applying a fixed percentage discount.
    """

    def __init__(self, name: str, percent: float):
        """
        Initializes a percent discount promotion.
        :param name: Name of the promotion.
        :type name: str
        :param percent: Discount percentage (e.g., 20 for 20%).
        :type percent: float
        """
        super().__init__(name)
        self._percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """
        Applies the percentage discount to the total price.
        :param product: The product being purchased.
        :type product: Product
        :param quantity: Quantity being purchased.
        :type quantity: int
        :return: Total discounted price.
        :rtype: float
        """
        total_price = product.price * quantity
        discount = total_price * (self._percent / 100)
        return total_price - discount
