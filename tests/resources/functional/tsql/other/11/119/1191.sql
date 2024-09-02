--Query type: DDL
CREATE TABLE Supplier (
    supplier_id INT NOT NULL,
    company_name VARCHAR(20),
    order_count INT,
    order_date DATE
) WITH (DISTRIBUTION = HASH(supplier_id));

INSERT INTO Supplier (
    supplier_id,
    company_name,
    order_count,
    order_date
)
VALUES
    (1, 'company1', 10, '2020-01-01'),
    (2, 'company2', 20, '2020-01-02');

SELECT *
FROM Supplier;