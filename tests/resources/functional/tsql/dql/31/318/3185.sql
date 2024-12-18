-- tsql sql:
SELECT c_customer_sk FROM (VALUES (1, '123456789'), (2, '987654321')) AS customer (c_customer_sk, c_phone) WHERE c_phone = '123456789';
