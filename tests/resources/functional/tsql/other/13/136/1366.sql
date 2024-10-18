--Query type: DDL
CREATE VIEW vw_CustomerInfo
AS
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS Customer (c_custkey, c_name, c_address);
-- REMORPH CLEANUP: DROP VIEW vw_CustomerInfo;