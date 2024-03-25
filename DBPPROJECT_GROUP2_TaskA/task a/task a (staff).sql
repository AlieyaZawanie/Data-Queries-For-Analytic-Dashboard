# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

#Total Staff in Each Store
CREATE VIEW staff_store_view AS
SELECT s.store_name, COUNT(st.staff_id) AS total_staff
FROM stores s JOIN staffs st ON s.store_id = st.store_id
GROUP BY s.store_name;
SELECT store_name, total_staff FROM staff_store_view;

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
SELECT store_name, CAST(customer_staff_ratio AS DECIMAL(10, 2)) AS customer_staff_ratio FROM ratio_store_view;

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
SELECT store_name, years, CAST(customer_staff_ratio AS DECIMAL(10, 2)) AS customer_staff_ratio FROM ratio_year_view;
