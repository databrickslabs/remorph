--Query type: TCL
WITH cte AS ( SELECT * FROM ( VALUES (1, 'John', 'USA', 'New York'), (2, 'Jane', 'Canada', 'Toronto') ) AS customers (customer_id, name, country, city) ) SELECT * FROM cte WHERE country = 'USA' AND city = 'New York' AND customer_id = 1;
