--Query type: DDL
SELECT * INTO quarterly_revenue FROM ( SELECT * FROM ( VALUES (1, 1, 100.00, 25.00, 25.00, 25.00, 25.00), (2, 2, 200.00, 50.00, 50.00, 50.00, 50.00) ) AS temp ( custkey, orderkey, total_revenue, q1, q2, q3, q4 ) ) AS temp_result; SELECT * FROM quarterly_revenue; -- REMORPH CLEANUP: DROP TABLE quarterly_revenue;
