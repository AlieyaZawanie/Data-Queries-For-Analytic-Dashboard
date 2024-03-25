# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

use bikestore;
SELECT * FROM bikestore.order_items;

 ## total sales value   
CREATE VIEW total_sales_view AS
SELECT CAST(SUM(total_sales) AS FLOAT) AS total_sales_sum FROM ( SELECT quantity * list_price * (1 - discount) AS total_sales FROM order_items) AS subquery1 ;

SELECT total_sales_sum FROM total_sales_view;


##total sales quantity
CREATE VIEW total_sales_q_view AS
SELECT CAST(SUM(quantity) AS SIGNED) AS total_quantity_ordered FROM order_items;

SELECT total_quantity_ordered FROM total_sales_q_view;

##sales by year and product
SELECT *
FROM order_items
JOIN orders
ON order_items.order_id = orders.order_id
JOIN products
ON order_items.product_id = products.product_id;



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
    p.product_name;
 
 
SELECT CAST(SUM(total_sales)AS FLOAT) , year  FROM total_sales_year_product_view AS subquery2 group by YEAR ;
SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year  FROM total_sales_year_product_view AS subquery2 group by product_name , year ;

SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year FROM total_sales_year_product_view AS subquery2 group by product_name HAVING year = 2016;
SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year FROM total_sales_year_product_view AS subquery2 group by product_name HAVING year = 2017;
SELECT CAST(SUM(total_sales)AS FLOAT) , product_name , year FROM total_sales_year_product_view AS subquery2 group by product_name HAVING year = 2018;

##select product with max sales
SELECT product_name, year, CAST(MAX(total_sales)AS FLOAT)  FROM total_sales_year_product_view GROUP BY product_name, year ORDER BY total_sales DESC LIMIT 1;
