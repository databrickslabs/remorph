--Query type: DQL
WITH customer_obj AS (
    SELECT OBJECT_ID(N'customer') AS obj_id
)
SELECT OBJECTPROPERTYEX(obj_id, N'BaseType') AS [Customer Base Type]
FROM customer_obj;
