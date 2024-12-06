-- tsql sql:
CREATE TABLE Customer (id INT, name VARCHAR(50));
CREATE TABLE Customer_new (id INT, name VARCHAR(50));
EXEC sp_rename 'Customer_new', 'Customer_old';
EXEC sp_rename 'Customer', 'Customer_new';
DROP TABLE Customer_old;
SELECT * FROM Customer_new;
-- REMORPH CLEANUP: DROP TABLE Customer_new;
-- REMORPH CLEANUP: DROP PROCEDURE sp_rename;
