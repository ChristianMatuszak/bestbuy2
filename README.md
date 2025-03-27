# BestBuy Inventory System

## Description
This project simulates a simple inventory system for an online store. It includes two main classes:

- **`Product`**: Manages products, including their prices and quantities in stock.
- **`Store`**: Manages a list of products and allows users to add or remove products, make orders, and view the total quantity of products in the store.
- **`Promotion`**: A new feature that enables applying discounts to products using reusable promotion strategies.

### Learning Project
This is a **learning project** that demonstrates object-oriented programming (OOP) principles in Python. It focuses on creating and managing classes, handling product inventories, and simulating transactions in a store environment.

## Features

### Product Management
- Products can be added or removed from the store.
- The total quantity of all products in the store can be calculated.
- The store displays all available products with current stock, prices, and active promotions.

### Promotions (New)
- Products can have a promotion assigned (only one at a time).
- Available promotions include:
  - **Second Half Price**: Every second item is 50% off.
  - **Buy 2, Get 1 Free**: Every third item is free.
  - **Percentage Discount**: e.g. 30% off.
- Promotions are automatically applied during checkout.
- Promotion names are displayed alongside product details.

### Ordering
- Users can place an order by selecting products and specifying quantities.
- The total price of the order is calculated automatically.
- Applied promotions are factored into the final price.
- Ordering flow resets properly between transactions to prevent carry-over.

## Usage
Run the `main.py` file to interact with the inventory system:

```bash
python main.py
