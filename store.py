from products import Product
from typing import List


class Store:
    """
    Represents a store that manages products in an inventory system.
    Attributes:
        products (List[Product]): A list of products available in the store.
    """

    def __init__(self, products=None):
        """
        Initializes the store with a list of products.
        :param products: List of products to initialize the store with. Defaults to an empty list.
        :type products: List[Product]
        :return: None
        """
        if products is None:
            products = []
        self.products = products


    def add_product(self, product):
        """
        Adds a new product to the list if it is not already in there
        :param product: the product to be added
        :type product: Product
        :return: prints a message confirming the addition
        """
        if not isinstance(product, Product):
            raise ValueError("Invalid input: product must be an instance of the Product class")

        if product in self.products:
            raise ValueError(f"Product {product} already in list.")
        self.products.append(product)


    def remove_product(self, product):
        """"
        Checks if the product that needs to be removed is inside the list.
        And removes it if found
        :param product: the product to be removed
        :type product: Product
        :return: True if the product was successfully removed, False if not found.
        :rtype: bool
        """
        if product in self.products:
            self.products.remove(product)
            return True
        return False


    def get_total_quantity(self) -> int:
        """
        Calculates the total quantity of all products in the store.
        :return: The total sum of all product quantities.
        :rtype: int
        """
        return sum(product.quantity for product in self.products)


    def get_all_products(self) -> List[Product]:
        """
        iterates through the list and collects every active product and returns it inside the list
        :return: A list of all active products in store
        :rtype: List
        """
        return [product for product in self.products if product.active]


    def order(self, shopping_list) -> float:
        """
        Calculate the total price of all bought products
        :param shopping_list: List of Tuples with 2 items (product, buys)
        :return: total price of all bought products
        :rtype: float
        """
        total_price = 0.0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price