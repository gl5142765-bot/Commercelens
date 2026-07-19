# Day 6 – Gold SQL Questions, Outputs, and Chart Use

For each business question, we document:
- User question
- SQL query - Expected output columns
- Whether charting may be useful

---

## Question 1
User question:
What is the total revenue for the selected period?

SQL query:
query = """
SELECT
  SUM(sale_price) AS total_revenue
FROM order_items
WHERE created_at BETWEEN '2022-01-01' AND '2023-12-31';
"""


Expected output columns (1 column):
total_revenue

Charting useful?
No – single summary metric; better as a KPI or table cell than a chart. 

---

## Question 2
User question:
How many orders were placed in the selected period?

SQL query:
query = """
SELECT
  COUNT(order_id) AS order_count
FROM orders
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
"""

Expected output columns (1 column):
order_count

Charting useful?
No – single count for the chosen period; suitable as a KPI or table.

---

## Question 3
User question:
What is the average order value?

SQL query:
query = """
SELECT
  SUM(sale_price) * 1.0 / COUNT(DISTINCT order_id) AS average_order_value
FROM order_items
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
"""

Expected output columns (1 column):
average_order_value

Charting useful?
No – single AOV for the period; best as a KPI. 

---

## Question 4
User question:
What is the average number of items per order?

SQL query:
query = """
SELECT
  AVG(num_of_item * 1.0) AS avg_items_per_order
FROM orders
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
"""


Expected output columns (1 column):
average_items_per_order

Charting useful?
No – single efficiency metric, KPI or table. 

---

## Question 5
User question:
How has total revenue changed over time?

SQL query:
query = """
SELECT
  strftime('%Y-%m', created_at) AS month,
  SUM(sale_price) AS total_revenue
FROM order_items
WHERE created_at BETWEEN '2022-01-01' AND '2024-12-31'
GROUP BY strftime('%Y-%m', created_at)
ORDER BY month;
"""


import matplotlib.pyplot as plt


# Optional: check the first few rows
result.head()

# Create a line chart of monthly total revenue
plt.figure(figsize=(10, 5))
plt.plot(result["month"], result["total_revenue"], marker="o")
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Total revenue")
plt.title("Monthly total revenue (2022–2024)")
plt.tight_layout()
plt.show()

Expected output columns (2 columns):
period (for example, month or day)
total_revenue

Charting useful?
Yes – time series of revenue; line or bar chart over time. 

---

## Question 6
User question:
How has the order count changed over time?

SQL query:
query = """
SELECT
  strftime('%Y-%m', created_at) AS month,
  COUNT(order_id) AS order_count
FROM orders
WHERE created_at BETWEEN '2022-01-01' AND '2024-12-31'
GROUP BY strftime('%Y-%m', created_at)
ORDER BY month;
"""
import matplotlib.pyplot as plt

# Run the SQL and get monthly order counts
result_q6 = pd.read_sql_query(query, conn)  # assumes 'query' is the SQL above

# Optional: inspect
result_q6.head()

# Create a line chart of monthly order count
plt.figure(figsize=(10, 5))
plt.plot(result_q6["month"], result_q6["order_count"], marker="o", color="orange")
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Order count")
plt.title("Monthly order count (2022–2024)")
plt.tight_layout()
plt.show()

Expected output columns (2 columns):
period (for example, month or day)
order_count

Charting useful?
Yes – time series of counts; line or bar chart.

---

## Question 7
User question:
How has average order value changed over time?

SQL query:
query = """
SELECT
  strftime('%Y-%m', created_at) AS month,
  SUM(sale_price) AS total_revenue,
  COUNT(DISTINCT order_id) AS order_count,
  SUM(sale_price) * 1.0 / COUNT(DISTINCT order_id) AS average_order_value
FROM order_items
WHERE created_at BETWEEN '2023-01-01' AND '2024-12-31'
GROUP BY strftime('%Y-%m', created_at)
ORDER BY month;
"""

# Run the SQL and get monthly AOV plus supporting metrics
result_q7 = pd.read_sql_query(query, conn)  # assumes 'query' is the SQL above

# Optional: see table of month, revenue, orders, AOV
result_q7.head()

# Create a line chart of monthly average order value
plt.figure(figsize=(10, 5))
plt.plot(result_q7["month"], result_q7["average_order_value"], marker="o", color="green")
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Average order value")
plt.title("Monthly average order value (2023–2024)")
plt.tight_layout()
plt.show()


Expected output columns (4 columns):
period (for example, month)
total_revenue
order_count
average_order_value



Charting useful?
Yes – line chart of average order value over time, with table for supporting metrics.
---

## Question 8
User question:
How has the number of items per order changed over time?

SQL query:
query = """
SELECT
  strftime('%Y-%m', created_at) AS month,
  COUNT(order_id) AS order_count,
  SUM(num_of_item) AS total_items,
  SUM(num_of_item) * 1.0 / COUNT(order_id) AS avg_items_per_order
FROM orders
WHERE created_at BETWEEN '2023-01-01' AND '2024-12-31'
GROUP BY strftime('%Y-%m', created_at)
ORDER BY month;
"""

result_q8 = pd.read_sql_query(query, conn)  # assumes 'query' is the SQL above

# Optional: inspect the table
result_q8.head()

# Create a line chart of average items per order over time
plt.figure(figsize=(10, 5))
plt.plot(result_q8["month"], result_q8["avg_items_per_order"], marker="o", color="purple")
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Average items per order")
plt.title("Monthly average items per order (2023–2024)")
plt.tight_layout()
plt.show()

Expected output columns (4 columns):
period (for example, month)
total_items
order_count
average_items_per_order

Charting useful?
Yes – line chart of average items per order over time, plus supporting table. 

---

## Question 9
User question:
Which month had the highest revenue?

SQL query:
query = """
SELECT
  month,
  total_revenue
FROM (
  SELECT
    strftime('%Y-%m', created_at) AS month,
    SUM(sale_price) AS total_revenue
  FROM order_items
  WHERE created_at BETWEEN '2022-01-01' AND '2022-12-31'
  GROUP BY strftime('%Y-%m', created_at)
) AS monthly_rev
ORDER BY total_revenue DESC
LIMIT 1;
"""

Expected output columns (1 column):
month_with_highest_revenue
(or month and total_revenue if you decide to return both)

Charting useful?
As a single row: No – it is a max finder and fits a table or KPI.  
If extended to “show revenue for all months” and highlight the highest, then charting becomes useful as a bar or line chart with the max highlighted.

---

## Question 10
User question:
Which month had the highest order count?

SQL query:
query = """
SELECT
  month,
  order_count
FROM (
  SELECT
    strftime('%Y-%m', created_at) AS month,
    COUNT(order_id) AS order_count
  FROM orders
  WHERE created_at BETWEEN '2022-01-01' AND '2024-12-31'
  GROUP BY strftime('%Y-%m', created_at)
) AS monthly_orders
ORDER BY order_count DESC
LIMIT 1;
"""

Expected output columns (1 column):
month_with_highest_order_count
(or month and order_count if you return both)

Charting useful?
As a single row: No – better as a table or KPI.  
If expanded to show order count for all months, then charting is useful. 

---

## Question 11
User question:
Which month had the highest average order value?

SQL query:
query = """
SELECT
  month,
  average_order_value
FROM (
  SELECT
    strftime('%Y-%m', created_at) AS month,
    SUM(sale_price) AS total_revenue,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(sale_price) * 1.0 / COUNT(DISTINCT order_id) AS average_order_value
  FROM order_items
  WHERE created_at BETWEEN '2022-01-01' AND '2024-12-31'
  GROUP BY strftime('%Y-%m', created_at)
) AS monthly_aov
ORDER BY average_order_value DESC
LIMIT 1;
"""

Expected output columns (1 column):
month_with_highest_average_order_value
(or month and average_order_value)

Charting useful?
As a single row: No.  
As a full average-order-value-by-month series: Yes, line chart with highlighted max. 

---

## Question 12
User question:
Which month had the largest orders on average?

SQL query:
query = """
SELECT
  month,
  average_order_value
FROM (
  SELECT
    strftime('%Y-%m', created_at) AS month,
    SUM(sale_price) AS total_revenue,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(sale_price) * 1.0 / COUNT(DISTINCT order_id) AS average_order_value
  FROM order_items
  GROUP BY strftime('%Y-%m', created_at)
) AS monthly_aov
ORDER BY average_order_value DESC
LIMIT 1;
"""

Expected output columns (1 column):
month_with_largest_orders_on_average
(or month and the chosen “average size” metric)

Charting useful?
As a single row: No.  
If interpreted as “show the chosen average size metric by month, then highlight the max”, charting is useful. 

metric ambiguities'
none(as fixed in SQL query)