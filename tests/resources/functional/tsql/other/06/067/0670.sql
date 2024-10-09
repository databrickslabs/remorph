--Query type: DML
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'customer_table')
CREATE TABLE customer_table
(
    customer_ID INT,
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    address_ID INT
);

INSERT INTO customer_table (customer_ID, last_name, first_name, address_ID)
SELECT * FROM (
    VALUES 
        (201, 'Smith', 'John', 1),
        (202, 'Johnson', 'Mary', 2),
        (203, 'Williams', 'David', 3)
) AS temp_result (customer_ID, last_name, first_name, address_ID);

SELECT * FROM customer_table;

-- REMORPH CLEANUP: DROP TABLE customer_table;