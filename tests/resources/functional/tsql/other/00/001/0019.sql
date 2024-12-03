--Query type: DML
CREATE TABLE products (product_ID INTEGER, wholesale_price REAL);
INSERT INTO products (product_ID, wholesale_price)
SELECT product_ID, wholesale_price
FROM (VALUES (1, 1.00), (2, 2.00)) AS products(product_ID, wholesale_price);
