--Query type: DDL
WITH price_view AS ( SELECT 1 AS id, 1500 AS price WHERE 1500 >= 1000 AND 1500 < 20000 ) SELECT * FROM price_view;
