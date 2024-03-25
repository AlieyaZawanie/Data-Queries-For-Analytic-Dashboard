# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

queryT1 = 'SELECT count(*) FROM customers'
queryT2 = 'SELECT count(*) FROM products'
queryT3 = 'SELECT count(*) FROM stores'
queryT4 = 'SELECT count(*) FROM orders'
queryT5 = 'SELECT YEAR(order_Date) as year,  count(*) as no_of_orders FROM orders GROUP BY YEAR(order_Date)'
queryT6 = 'SELECT store_id as store, count(*) as no_of_orders FROM orders GROUP BY store_id'

##CREATE VIEW total_sales_view AS
##SELECT CAST(SUM(total_sales) AS FLOAT) AS total_sales_sum FROM ( SELECT quantity * list_price * (1 - discount) AS total_sales FROM order_items) AS subquery1 ;
queryT7 = 'SELECT total_sales_sum FROM total_sales_view'

##CREATE VIEW total_sales_q_view AS
##SELECT CAST(SUM(quantity) AS SIGNED) AS total_quantity_ordered FROM order_items;
queryT8 = 'SELECT total_quantity_ordered FROM total_sales_q_view'

'''
CREATE VIEW total_sales_year_product_view AS
SELECT 
    EXTRACT(YEAR FROM oi.order_date) AS year,
    p.product_name,
    SUM(oi.quantity * oi.list_price *  (1 - oi.discount)) AS total_sales
FROM 
    (
        SELECT 
            order_items.quantity, 
            order_items.discount,
            order_items.list_price, 
            order_items.product_id, 
            orders.order_date
        FROM 
            order_items
        JOIN 
            orders ON order_items.order_id = orders.order_id
    ) AS oi
JOIN 
    products p ON oi.product_id = p.product_id
GROUP BY 
    year, 
    p.product_name;'''
queryT9 = 'SELECT CAST(SUM(total_sales)AS FLOAT) , year  FROM total_sales_year_product_view AS subquery2 group by YEAR'
queryT10 = 'SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year  FROM total_sales_year_product_view AS subquery2 group by year , product_name '

queryT11 = 'SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year FROM total_sales_year_product_view AS subquery2 group by product_name HAVING year = 2016'
queryT12 = 'SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year FROM total_sales_year_product_view AS subquery2 group by product_name HAVING year = 2017'
queryT13 = 'SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year FROM total_sales_year_product_view AS subquery2 group by product_name HAVING year = 2018'

queryT14 = 'SELECT product_name, year, CAST(MAX(total_sales)AS FLOAT)  FROM total_sales_year_product_view GROUP BY product_name, year ORDER BY total_sales DESC LIMIT 1'

##CREATE VIEW total_customer_view AS
#SELECT COUNT(DISTINCT customer_id) AS TotalCustomers FROM customers;
queryT15 = 'SELECT TotalCustomers FROM total_customer_view'

'''CREATE VIEW total_customer_categorization_view AS
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
GROUP BY sub.customer_id, full_name;'''
queryT16 = 'SELECT COUNT(customer_id) AS NumberOfRecurringCustomers FROM total_customer_categorization_view WHERE Categorization = "Recurring"'
queryT17 = 'SELECT COUNT(customer_id) AS NumberOfRecurringCustomers FROM total_customer_categorization_view WHERE Categorization = "One-Time"'


'''CREATE VIEW list_recurring_customer_sales_view AS
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
GROUP BY recurring_customers.customer_id, recurring_customers.RecurringCustomers;'''
queryT18 = 'SELECT customer_id , RecurringCustomers , total_sales AS ListRecurringCustomers FROM list_recurring_customer_sales_view'


'''CREATE VIEW list_onetime_customer_sales_view AS
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
GROUP BY ot_customers.customer_id, ot_customers.OneTimeCustomers;'''
queryT19 = 'SELECT customer_id , OneTimeCustomers , total_sales AS ListOneTimeCustomers FROM list_onetime_customer_sales_view'


'''CREATE VIEW list_top10_customer_sales_view AS
SELECT 
    customers.customer_id, 
    CONCAT(customers.first_name, ' ', customers.last_name) AS full_name, 
    SUM(order_items.quantity * order_items.list_price * (1 - order_items.discount)) AS total_sales
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY customers.customer_id, full_name
ORDER BY total_sales DESC
LIMIT 10;'''

queryT20 = 'SELECT customer_id , full_name , total_sales AS Listtop10Customers FROM list_top10_customer_sales_view'

'''
--------------------------Item Dashboard--------------------------
# Total products

CREATE VIEW total_product_view AS
SELECT COUNT(*) AS total_product FROM products;
'''
queryT21 = 'SELECT total_product FROM total_product_view;'

'''
# Total brands

CREATE VIEW total_brands_view AS
SELECT COUNT(*) AS total_brands FROM brands;
'''
queryT22 = 'SELECT total_brands FROM total_brands_view;'

'''
#Distribution of products according to different brands.

CREATE VIEW distribution_products_view AS
SELECT b.brand_name, COUNT(p.product_id) AS product_count
FROM brands b
JOIN products p ON b.brand_id = p.brand_id
GROUP BY b.brand_name
ORDER BY product_count DESC;
'''
queryT23 = 'SELECT brand_name, product_count FROM distribution_products_view;'

'''
#Brands that have the most sales and its product
##Brand that has the most sales

CREATE VIEW brand_sales_view AS
SELECT b.brand_name, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
GROUP BY b.brand_name
ORDER BY total_sales DESC;
'''
queryT24 = 'SELECT brand_name, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM brand_sales_view;'

'''
##Brand and its Product that has the most sales

CREATE VIEW brand_sales_product_view AS
WITH BrandProductSales AS (
    SELECT
        b.brand_name, p.product_name, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales,
        ROW_NUMBER() OVER(PARTITION BY b.brand_name ORDER BY SUM(oi.quantity * oi.list_price * (1 - oi.discount)) DESC) AS sales_rank
    FROM
        order_items oi
    JOIN
        products p ON oi.product_id = p.product_id
    JOIN
        brands b ON p.brand_id = b.brand_id
    GROUP BY
        b.brand_name, p.product_name
)
SELECT
    brand_name, product_name, total_sales
FROM
    BrandProductSales
WHERE
    sales_rank = 1
ORDER BY total_sales DESC;
'''
queryT25 = 'SELECT brand_name, product_name, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM brand_sales_product_view;'

'''
#Item by Price Category

CREATE VIEW categorized_items_view AS
SELECT oi.order_id, oi.item_id, p.product_name,
	CASE
		WHEN oi.list_price < 500 THEN 'Low-Priced'
        WHEN oi.list_price >= 500 AND oi.list_price <= 1000 THEN 'Medium-Priced'
        WHEN p.list_price > 1000 THEN 'High-priced'
		ELSE 'Others'
	END AS price_category,
    oi.quantity * oi.list_price * (1 - oi.discount) AS total_sales
FROM order_items oi JOIN products p ON oi.product_id = p.product_id
GROUP BY oi.order_id, oi.item_id
ORDER BY oi.order_id, oi.item_id ASC;
'''
queryT26 = 'SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view;'
queryT27 = 'SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view WHERE price_category = "Low-Priced";'
queryT28 = 'SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view WHERE price_category = "Medium-Priced";'
queryT29 = 'SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view WHERE price_category = "High-Priced";'

'''
#Top 5 Product Sales by Price Category

CREATE VIEW top5_view AS
WITH RankedSales AS (
    SELECT
	p.product_id,
        p.product_name,
        CASE
            WHEN oi.list_price < 500 THEN 'Low-Priced'
            WHEN oi.list_price >= 500 AND oi.list_price <= 1000 THEN 'Medium-Priced'
            ELSE 'High-Priced'
        END AS price_category,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales,
        ROW_NUMBER() OVER (PARTITION BY
            CASE
                WHEN oi.list_price < 500 THEN 'Low-Priced'
                WHEN oi.list_price >= 500 AND oi.list_price <= 1000 THEN 'Medium-Priced'
                ELSE 'High-Priced'
            END
            ORDER BY SUM(oi.quantity * oi.list_price * (1 - oi.discount)) DESC
        ) AS rank_within_category
    FROM
        order_items oi
    JOIN
        products p ON oi.product_id = p.product_id
    GROUP BY
        price_category, p.product_id, p.product_name
    ORDER BY
        price_category, total_sales DESC
)
SELECT
    product_name,
    price_category,
    total_sales
FROM
    RankedSales
WHERE
    rank_within_category <= 5
ORDER BY
    price_category, rank_within_category;
'''
queryT30 = 'SELECT product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM top5_view WHERE price_category = "Low-Priced";'

queryT31 =  'SELECT product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM top5_view WHERE price_category = "Medium-Priced";'

queryT32 = 'SELECT product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM top5_view WHERE price_category = "High-Priced";'

'''
--------------------------Staff Dashboard--------------------------

#Total Staff in Each Store

CREATE VIEW staff_store_view AS
SELECT s.store_name, COUNT(st.staff_id) AS total_staff
FROM stores s JOIN staffs st ON s.store_id = st.store_id
GROUP BY s.store_name;
'''
queryT33 = 'SELECT store_name, total_staff FROM staff_store_view;'

'''
#Customer to Staff Ratio by Store

CREATE VIEW ratio_store_view AS
SELECT s.store_name,
COUNT(DISTINCT c.customer_id) AS total_customers,
COUNT(DISTINCT st.staff_id) AS total_staff,
COUNT(DISTINCT c.customer_id)/COUNT(DISTINCT st.staff_id) AS customer_staff_ratio
FROM stores s
LEFT JOIN staffs st ON s.store_id = st.store_id
LEFT JOIN orders o ON s.store_id = o.store_id
LEFT JOIN customers c ON o.customer_id = c.customer_id
GROUP BY s.store_id;
'''
queryT34 = 'SELECT store_name, CAST(customer_staff_ratio AS DECIMAL(10, 2)) AS customer_staff_ratio FROM ratio_store_view;'

'''
#Customer to Staff Ratio by Year

CREATE VIEW ratio_year_view AS
SELECT s.store_name, YEAR(o.order_date) AS years,
COUNT(DISTINCT c.customer_id) AS total_customers,
COUNT(DISTINCT st.staff_id) AS total_staff,
COUNT(DISTINCT c.customer_id)/COUNT(DISTINCT st.staff_id) AS customer_staff_ratio
FROM stores s
LEFT JOIN staffs st ON s.store_id = st.store_id
LEFT JOIN orders o ON s.store_id = o.store_id
LEFT JOIN customers c ON o.customer_id = c.customer_id
GROUP BY s.store_id, years;
'''
queryT35 = 'SELECT store_name, years, CAST(customer_staff_ratio AS DECIMAL(10, 2)) AS customer_staff_ratio FROM ratio_year_view;'