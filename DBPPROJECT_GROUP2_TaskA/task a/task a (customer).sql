# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

##select total number of customers
CREATE VIEW total_customer_view AS
SELECT COUNT(DISTINCT customer_id) AS TotalCustomers FROM customers;
SELECT TotalCustomers FROM total_customer_view;

##categorizing customers
SELECT *
FROM customers
JOIN orders
ON customers.customer_id = orders.customer_id;

CREATE VIEW total_customer_categorization_view AS
SELECT sub.customer_id, sub.order_id , CONCAT(sub.first_name, ' ', sub.last_name) AS full_name,
CASE 
    WHEN COUNT(sub.order_id) > 1 THEN 'Recurring'
    ELSE 'One-Time'
END as Categorization
FROM 
    (SELECT customers.customer_id, first_name, last_name, order_id
    FROM customers
    JOIN orders
    ON customers.customer_id = orders.customer_id) as sub
GROUP BY sub.customer_id, full_name;

SELECT COUNT(customer_id) AS NumberOfRecurringCustomers FROM total_customer_categorization_view WHERE Categorization = 'Recurring';
SELECT customer_id , full_name AS RecurringCustomers FROM total_customer_categorization_view WHERE Categorization = 'Recurring';

SELECT COUNT(customer_id) AS NumberOfRecurringCustomers FROM total_customer_categorization_view WHERE Categorization = 'One-Time';
SELECT customer_id , full_name AS RecurringCustomers FROM total_customer_categorization_view WHERE Categorization = 'One-Time';

##list of recurring customers and their sales

##CREATE VIEW recurring_customer_sales_view AS
CREATE VIEW list_recurring_customer_sales_view AS
SELECT 
    recurring_customers.customer_id, 
    recurring_customers.RecurringCustomers, 
    SUM(order_items.quantity * order_items.list_price * (1 - order_items.discount)) AS total_sales
FROM 
    (SELECT customer_id, full_name AS RecurringCustomers 
     FROM total_customer_categorization_view 
     WHERE Categorization = 'Recurring') as recurring_customers
JOIN orders ON recurring_customers.customer_id = orders.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY recurring_customers.customer_id, recurring_customers.RecurringCustomers;

SELECT customer_id , RecurringCustomers , total_sales AS ListRecurringCustomers FROM list_recurring_customer_sales_view ;

CREATE VIEW list_onetime_customer_sales_view AS
SELECT 
    ot_customers.customer_id, 
    ot_customers.OneTimeCustomers, 
    SUM(order_items.quantity * order_items.list_price * (1 - order_items.discount)) AS total_sales
FROM 
    (SELECT customer_id, full_name AS OneTimeCustomers 
     FROM total_customer_categorization_view 
     WHERE Categorization = 'One-Time') as ot_customers
JOIN orders ON ot_customers.customer_id = orders.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY ot_customers.customer_id, ot_customers.OneTimeCustomers;

SELECT customer_id , OneTimeCustomers , total_sales AS ListOneTimeCustomers FROM list_onetime_customer_sales_view ;

##top 10 highest sales

CREATE VIEW list_top10_customer_sales_view AS
SELECT 
    customers.customer_id, 
    CONCAT(customers.first_name, ' ', customers.last_name) AS full_name, 
    SUM(order_items.quantity * order_items.list_price * (1 - order_items.discount)) AS total_sales
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY customers.customer_id, full_name
ORDER BY total_sales DESC
LIMIT 10;

SELECT customer_id , full_name , total_sales AS Listtop10Customers FROM list_top10_customer_sales_view ;
