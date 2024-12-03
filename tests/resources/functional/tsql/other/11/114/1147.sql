--Query type: DDL
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Customer')
BEGIN
    EXEC('CREATE SCHEMA Customer');
END
CREATE SEQUENCE Customer.CountBy5
  START WITH 5
  INCREMENT BY 5;
-- REMORPH CLEANUP: DROP SEQUENCE Customer.CountBy5;
-- REMORPH CLEANUP: DROP SCHEMA Customer;
