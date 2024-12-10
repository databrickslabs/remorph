-- tsql sql:
WITH temp_result AS ( SELECT totalprice, discount FROM orders ) SELECT totalprice + 10 + discount FROM temp_result GROUP BY totalprice + discount;
