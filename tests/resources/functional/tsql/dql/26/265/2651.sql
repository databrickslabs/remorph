-- tsql sql:
SELECT JSON_OBJECT('customer_name': c_name, 'address': JSON_OBJECT('street': c_street, 'city': c_city)) AS customer_info FROM (VALUES ('Customer1', '123 Main St', 'New York'), ('Customer2', '456 Elm St', 'Chicago')) AS customers (c_name, c_street, c_city)
