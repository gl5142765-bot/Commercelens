day03

## Core Business Tables
The core business tables are `users`, `products`, `orders`, and `order_items`. These tables store customer details, product details, order details, and item-level order details.

## Common Columns
- `id` in `users`.
- `user_id` in `orders`.
- `order_id` in `orders` and `order_items`.
- `product_id` in `products` and `order_items`.

## Simple Schema Link
- `users.id` links to `orders.user_id`.
- `orders.order_id` links to `order_items.order_id`.
- `products.id` links to `order_items.product_id`.

## Keys
- `users`: primary key = `id`.
- `products`: primary key = `id`.
- `orders`: primary key = `order_id`, foreign key = `user_id`.
- `order_items`: foreign keys = `order_id`, `product_id`.

## Business Meaning
- `users`: basic customer information, including user details, traffic source, and when the person became a user.
- `products`: product details such as name, category, brand, price, cost of making, SKU, and distribution center ID.
- `orders`: order-level information such as user ID, order date, item count, and status.
- `order_items`: item-level details for each order, tracking the product through ordering to delivery, including sale price and return status if applied.