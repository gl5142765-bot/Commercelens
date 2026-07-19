# Day 8 – Prompt Design and Schema Context

## Goal
Prepare the backend intelligence layer before coding the API by defining the schema context, metric definitions, and prompt template.

## Core Business Tables
The core business tables are `users`, `products`, `orders`, and `order_items`.

These tables store customer details, product details, order details, and item-level order details.

## Table Meaning
- `users`: customer profile details and acquisition information.
- `products`: product catalog information such as name, category, brand, price, cost, SKU, and distribution center.
- `orders`: order-level information such as user ID, order date, item count, and order status.
- `order_items`: item-level transaction details such as order ID, product ID, sale price, shipping and delivery timestamps, and return status.

## Keys and Relationships
- `users.id` links to `orders.user_id`
- `orders.order_id` links to `order_items.order_id`
- `products.id` links to `order_items.product_id`

# Day 8 – Prompt Design and Schema Context

## Goal
Prepare the backend intelligence layer before coding the API by defining the schema context, metric definitions, and the first prompt template.

## Core Business Tables
The core business tables are `users`, `products`, `orders`, and `order_items`.

These tables store customer details, product details, order details, and item-level order details.

## Table Meaning
- `users`: customer profile details and acquisition information.
- `products`: product catalog information such as name, category, brand, price, cost, SKU, and distribution center.
- `orders`: order-level information such as user ID, order date, item count, and order status.
- `order_items`: item-level transaction details such as order ID, product ID, sale price, shipping and delivery timestamps, and return status.

## Keys and Relationships
- `users.id` links to `orders.user_id`
- `orders.order_id` links to `order_items.order_id`
- `products.id` links to `order_items.product_id`

## Core Metrics
We finalized 4 core metrics for CommerceLens:

- Total revenue → sum of `sale_price`
- Order count → total number of orders
- Average order value → total revenue divided by order count
- Number of items per order → `num_of_item` from the `orders` table

## Expected Query Behavior
The model should generate SQL only.

Do not return explanations, markdown, or code fences unless explicitly requested.

## Prompt Template
You are an expert SQL assistant for the CommerceLens e-commerce dataset.

Use only the provided schema context to generate SQL queries.
Follow the metric definitions exactly.
Return SQL only.

Schema:
- users
- products
- orders
- order_items

Relationships:
- users.id = orders.user_id
- orders.order_id = order_items.order_id
- products.id = order_items.product_id

Metric definitions:
- Total revenue = sum of `sale_price`
- Order count = total number of orders
- Average order value = total revenue / order count
- Number of items per order = `num_of_item` from the `orders` table

Output rules:
- Return SQL only
- Do not add explanations
- Do not guess columns that are not in the schema
- Use the correct joins based on the schema
- Use date filters only when the question asks for a time period