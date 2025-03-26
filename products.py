class Product:
    """
    Represents a product in an inventory system.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product (must be non-negative).
        quantity (int): The available stock quantity (must be non-negative).
        active (bool): Indicates whether the product is available for sale.
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

    def __str__(self):
        """
        Returns a user-friendly string representation of the product.
        :return: A string that includes the product name and price
        :rtype: str
        """
        return f"{self.name} (Price: {self.price:.2f}€)"

    def get_quantity(self) -> int:
        """
        Returns the quantity of the product.
        :return: Quantity of the product.
        :rtype: int
        """
        return self.quantity

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
        :return: True if the product is successfully activated, otherwise False.
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

    def show(self) -> str:
        """
        Returns a formatted string with product details.
        :return: A formatted string containing the product name, price, and quantity.
        :rtype: str
        """
        return f"{self.name}, Price: {self.price:.2f}, Quantity: {self.quantity}"

    def buy(self, quantity) -> float:
        """
        Buys a given quantity of the product if it is available.
        Calculates the total purchase price and updates the quantity.
        If the quantity reaches 0 after the purchase, the product will be deactivated.

        :param quantity: The quantity to be purchased.
        :type quantity: int
        :return: The total price of the purchase.
        :rtype: float
        :raises ValueError: If the quantity is invalid or not enough stock is available.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Invalid input: quantity should be a positive integer")
        elif quantity > self.quantity:
            raise ValueError("Not enough stock available")

        total_price = quantity * self.price
        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        return total_price