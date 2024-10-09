--Query type: DML
CREATE TABLE new_customers
(
    first_name nvarchar(50),
    last_name nvarchar(50),
    phone_number nvarchar(20),
    address nvarchar(100),
    postal_code nvarchar(10)
);

INSERT INTO new_customers
(
    first_name,
    last_name,
    phone_number,
    address,
    postal_code
)
SELECT
    first_name,
    last_name,
    phone_number,
    NULL,
    postal_code
FROM
(
    VALUES
    (
        'John',
        'Doe',
        '123-456-7890',
        '123 Main St',
        '12345'
    ),
    (
        'Jane',
        'Doe',
        '987-654-3210',
        '456 Elm St',
        '67890'
    )
) AS temp
(
    first_name,
    last_name,
    phone_number,
    address,
    postal_code
)
WHERE
    phone_number LIKE '%123%';

SELECT * FROM new_customers;
-- REMORPH CLEANUP: DROP TABLE new_customers;