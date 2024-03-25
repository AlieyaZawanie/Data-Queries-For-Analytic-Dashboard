# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

# Total products
CREATE VIEW total_product_view AS
SELECT COUNT(*) AS total_product FROM products;
SELECT total_product FROM total_product_view;

# Total brands
CREATE VIEW total_brands_view AS
SELECT COUNT(*) AS total_brands FROM brands;
SELECT total_brands FROM total_brands_view;

#Distribution of products according to different brands.
CREATE VIEW distribution_products_view AS
SELECT b.brand_name, COUNT(p.product_id) AS product_count
FROM brands b
JOIN products p ON b.brand_id = p.brand_id
GROUP BY b.brand_name
ORDER BY product_count DESC;
SELECT brand_name, product_count FROM distribution_products_view;

#Brands that have the most sales and its product
##Brand that has the most sales
CREATE VIEW brand_sales_view AS
SELECT b.brand_name, SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
GROUP BY b.brand_name
ORDER BY total_sales DESC;
SELECT brand_name, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM brand_sales_view;

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
SELECT brand_name, product_name, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM brand_sales_product_view;

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
SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view;
SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view WHERE price_category = "Low-Priced";
SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view WHERE price_category = "Medium-Priced";
SELECT order_id, item_id, product_name, price_category, CAST(total_sales AS DECIMAL(10, 2)) AS total_sales FROM categorized_items_view WHERE price_category = "High-Priced";

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
SELECT product_name, price_category, total_sales FROM top5_view WHERE price_category = "Low-Priced";
SELECT product_name, price_category, total_sales FROM top5_view WHERE price_category = "Medium-Priced";
SELECT product_name, price_category, total_sales FROM top5_view WHERE price_category = "High-Priced";
