-- tsql sql:
WITH customer_cte AS ( SELECT CAST(c_customer_sk AS INT) AS Customer_SID FROM ( VALUES (1), (2), (3) ) AS customer(c_customer_sk) ) SELECT Customer_SID FROM customer_cte WHERE Customer_SID = 1
