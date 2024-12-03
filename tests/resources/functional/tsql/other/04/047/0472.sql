--Query type: DDL
WITH classified_columns AS ( SELECT 100.0 AS l_extendedprice, 0.1 AS l_discount UNION ALL SELECT 200.0, 0.2 ) SELECT l_extendedprice, l_discount FROM classified_columns;
