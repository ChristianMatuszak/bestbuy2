from colorama import Fore, Style
from store import Store
from products import Product, LimitedProduct, NonStockedProduct, SecondHalfPrice, ThirdOneFree, PercentDiscount


def main():
    """
    Initializes the store with a default product list and starts the interactive store menu.
    The menu allows users to view products, check store quantities, make orders, and quit the application.
    :return: None
    """
    # setup initial stock of inventory
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    NonStockedProduct("Windows License", price=125),
                    LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)
    best_buy = Store(product_list)
    start(best_buy)


def start(best_buy):
    """"
    Starts the interactive store menu where users can perform various actions such as:
    - Listing all products in the store
    - Displaying the total amount of products in the store
    - Making an order by selecting products and specifying quantities
    The function continuously prompts the user for input until they choose to quit.
    :param best_buy: The store object that manages the products and their interactions.
    :type best_buy: Store
    :return: None
    """
    while True:
        print("\n           Store Menu          ")
        print("          ------------         ")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "List all products in store")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "Show total amount in store")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "Make an order")
        print(Fore.GREEN + "4. " + Style.RESET_ALL + "Quit")

        user_choice = input("\nEnter your choice: ")

        if user_choice == "1":
            products = best_buy.get_all_products()
            for index, product in enumerate(products, start=1):
                promotion_info = f" - Promotion: {product.get_promotion().name}" if product.get_promotion() else ""

                if isinstance(product, NonStockedProduct):
                    print(f"{index}. {product.name} - Price: {product.price:.2f}€" + Fore.YELLOW + f"{promotion_info}" + Style.RESET_ALL)
                elif isinstance(product, LimitedProduct):
                    print(
                        f"{index}. {product.name} - Price: {product.price:.2f}€ - Quantity: {product.quantity} - Max: {product.maximum}" + Fore.YELLOW + f"{promotion_info}" + Style.RESET_ALL)
                else:
                    print(
                        f"{index}. {product.name} - Price: {product.price:.2f}€ - Quantity: {product.quantity}" + Fore.YELLOW + f"{promotion_info}" + Style.RESET_ALL)


        elif user_choice == "2":
            print(f"\nTotal quantity in store: {best_buy.get_total_quantity()}")

        elif user_choice == "3":
            shopping_list = []
            while True:
                print("\nAvailable Products:")
                for index, product in enumerate(best_buy.get_all_products(), start=1):
                    promotion_info = f" - Promotion: {product.get_promotion().name}" if product.get_promotion() else ""

                    if isinstance(product, NonStockedProduct):
                        print(f"{index}. {product.name} - Price: {product.price:.2f}€" + Fore.YELLOW + f"{promotion_info}" + Style.RESET_ALL)
                    elif isinstance(product, LimitedProduct):
                        print(
                            f"{index}. {product.name} - Price: {product.price:.2f}€ - Maximum: {product.maximum} per order" + Fore.YELLOW + f"{promotion_info}" + Style.RESET_ALL)
                    else:
                        print(
                            f"{index}. {product.name} - Price: {product.price:.2f}€ - Quantity: {product.quantity}" + Fore.YELLOW + f"{promotion_info}" + Style.RESET_ALL)

                product_choice = input("\nWhen you want to finish order, enter empty text.\nWhich product # do you want? ")

                if not product_choice:
                    break

                try:
                    if product_choice == "0":
                        raise ValueError(Fore.RED + "\nInvalid product number. Please try again." + Style.RESET_ALL)
                    product_index = int(product_choice) - 1
                    product = best_buy.get_all_products()[product_index]
                except (ValueError, IndexError):
                    print(Fore.RED + "\nInvalid product number. Please try again." + Style.RESET_ALL)
                    continue

                quantity = input(f"\nWhat amount do you want for {product.name}? ")

                try:
                    quantity = int(quantity)
                    if quantity <= 0:
                        print(Fore.RED + "\nQuantity must be a positive integer." + Style.RESET_ALL)
                        continue
                    if isinstance(product, LimitedProduct) and quantity > product.maximum:
                        print(Fore.RED + f"\nYou can only purchase a maximum of {product.maximum} units of {product.name}." + Style.RESET_ALL)
                        continue
                except ValueError:
                    print(Fore.RED + "\nPlease enter a valid quantity." + Style.RESET_ALL)
                    continue

                if not isinstance(product, NonStockedProduct) and quantity > product.quantity:
                    print(Fore.RED + "\nNot enough stock available!" + Style.RESET_ALL)
                    print(Fore.RED + f"Currently, there are {product.quantity} units available for {product.name}." + Style.RESET_ALL)
                    continue

                shopping_list.append((product, quantity))
                print(f"\nProduct added to list: {product.name} (x{quantity})")

            total_price = best_buy.order(shopping_list)
            print(f"\nTotal price of the order: " + Fore.GREEN + f"{total_price:.2f}€" + Style.RESET_ALL)

        elif user_choice == "4":
            print("\nBye!")
            return

        else:
            print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram terminated by user." + Style.RESET_ALL)