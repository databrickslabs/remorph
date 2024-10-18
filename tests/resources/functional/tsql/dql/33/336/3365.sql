--Query type: DQL
SELECT OBJECT_DEFINITION(OBJECT_ID(object_name)) AS [Customer Address Definition]
FROM (
    VALUES (N'customer.c_address')
) AS temp(object_name);