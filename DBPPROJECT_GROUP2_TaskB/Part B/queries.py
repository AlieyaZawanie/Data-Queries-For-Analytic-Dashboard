# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

# USE sakila;
#
# CREATE OR REPLACE VIEW film_details AS
# SELECT
# film.film_id,
# film.title,
# film.description,
# film.release_year,
# film.language_id,
# film.rental_duration,
# film.rental_rate,
# film.replacement_cost,
# film.length,
# film.rating,
# language.name AS language,
# GROUP_CONCAT(DISTINCT category.name ORDER BY category.name) AS categories
# FROM
# film
# JOIN
# language ON film.language_id = language.language_id
# JOIN
# film_category ON film.film_id = film_category.film_id JOIN category
# ON
# film_category.category_id = category.category_id
# GROUP BY
# film.film_id, film.title, film.description, film.release_year, film.length, language.name;

queryT1 = 'SELECT count(*) FROM customer'
queryT2 = 'SELECT count(*) FROM actor'
queryT3 = 'SELECT count(*) FROM film'
queryT4 = 'SELECT count(*) FROM staff'

queryT5 = 'SELECT COUNT(*) as customer_count, store_id FROM customer GROUP BY store_id'
queryT6 = '''
SELECT CONCAT(customer.first_name, ' ', customer.last_name) AS customer_name, 
       SUM(payment.amount) AS total_paid 
FROM customer 
JOIN payment ON customer.customer_id = payment.customer_id 
GROUP BY customer_name
ORDER BY total_paid DESC 
LIMIT 10
'''
queryT7 = 'SELECT COUNT(*) as customer_count, active FROM customer GROUP BY active'
queryT8 = 'SELECT city.country_id, COUNT(customer.customer_id) AS total_customers FROM customer JOIN address ON customer.address_id = address.address_id JOIN sakila.city ON address.city_id = city.city_id GROUP BY city.country_id ORDER BY total_customers DESC LIMIT 10'
queryT9 = 'SELECT country_id, country FROM country WHERE country_id IN (15, 23, 44, 45, 50, 60, 75, 80, 97, 103)'
queryT10 = 'SELECT MONTH(payment_date) AS month, SUM(amount) AS amount FROM payment GROUP BY month;'
queryT11 = '''
SELECT CONCAT(customer.first_name, ' ', customer.last_name) AS customer_name, 
COUNT(rental_id) AS film 
FROM customer 
JOIN rental ON customer.customer_id = rental.customer_id 
GROUP BY customer_name 
ORDER BY film DESC 
LIMIT 10
'''

queryT12 = '''SELECT 
        CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
        COUNT(fa.film_id) AS film_count
    FROM actor a
    JOIN film_actor fa ON a.actor_id = fa.actor_id
    GROUP BY a.actor_id
    ORDER BY film_count DESC
    LIMIT 10'''

queryT13 = 'SELECT name FROM category'

queryT14 = '''
    SELECT 
        CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
        COUNT(r.rental_id) AS total_rentals
    FROM
        actor a
        JOIN film_actor fa ON a.actor_id = fa.actor_id
        JOIN film f ON fa.film_id = f.film_id
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY
        actor_name
    ORDER BY
        total_rentals DESC
    LIMIT 10
'''

queryT15 = '''SELECT 
    CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
    ROUND(AVG(CAST(f.rental_rate AS DECIMAL(4, 2))), 2) AS avg_rental_rate
FROM
    actor a
    JOIN film_actor fa ON a.actor_id = fa.actor_id
    JOIN film f ON fa.film_id = f.film_id
WHERE
    f.rental_rate IS NOT NULL
GROUP BY
    actor_name
ORDER BY
    avg_rental_rate ASC
'''

queryT16 = '''
    SELECT 
        CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
        c.name AS film_category,
        COUNT(fa.film_id) AS film_count
    FROM actor a
    JOIN film_actor fa ON a.actor_id = fa.actor_id
    JOIN film f ON fa.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    GROUP BY actor_name, film_category
    ORDER BY RAND()
'''


queryT17 = '''
SELECT
    actor.actor_id,
    CONCAT(actor.first_name, ' ', actor.last_name) AS actor_name,
    COUNT(DISTINCT film_actor.film_id) AS movie_count
FROM
    actor
JOIN
    film_actor ON actor.actor_id = film_actor.actor_id
GROUP BY
    actor.actor_id, actor_name
ORDER BY
    movie_count DESC;
'''

queryT18 = 'SELECT COUNT(inventory_id) as inventory_count, store_id FROM inventory GROUP BY store_id'

queryT19 ='SELECT COUNT(film_id) as film, replacement_cost FROM film GROUP BY replacement_cost'

queryT20 ='SELECT store_id, COUNT(amount) as revenue FROM payment JOIN staff ON staff.staff_id = payment.staff_id GROUP BY staff.store_id'

rating_count = 'SELECT rating, COUNT(rating) AS rating_count FROM film_details GROUP BY rating;'
category_count = 'SELECT categories, COUNT(categories) AS category_count FROM film_details GROUP BY categories;'
rental_rate = 'SELECT rental_rate, COUNT(rental_rate) as rate FROM film_details GROUP BY rental_rate;'
rate_duration = 'SELECT rental_rate, rental_duration FROM film_details; '
top_category = 'SELECT title, categories AS Category, rental_duration AS Duration FROM film_details ORDER BY Duration DESC LIMIT 10'
low_category = 'SELECT title, categories AS Category, rental_duration AS Duration FROM film_details ORDER BY Duration ASC LIMIT 10'
