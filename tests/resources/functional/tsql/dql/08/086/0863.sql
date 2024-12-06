-- tsql sql:
WITH MY_CTE AS (SELECT * FROM (VALUES ('customer1', 10), ('customer2', 20)) AS CUSTOMER (C_NAME, C_ACCTBAL)) SELECT * FROM MY_CTE;
