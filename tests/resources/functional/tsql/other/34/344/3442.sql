--Query type: DCL
CREATE TABLE TPCHCustomer42
(
    CustomerName VARCHAR(50)
);

INSERT INTO TPCHCustomer42
(
    CustomerName
)
VALUES
(
    'TPCHCustomer42'
);

REVOKE CONTROL ON TPCHCustomer42 TO HamidS CASCADE;

SELECT *
FROM TPCHCustomer42;

-- REMORPH CLEANUP: DROP TABLE TPCHCustomer42;
