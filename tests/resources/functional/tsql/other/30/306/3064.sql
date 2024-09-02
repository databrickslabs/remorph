--Query type: DCL
SELECT * FROM (VALUES ('customer', 1), ('orders', 2)) AS database_objects(object_name, object_id);