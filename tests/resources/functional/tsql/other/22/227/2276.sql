--Query type: DCL
CREATE TYPE Customer.Address AS TABLE (AddressID int, AddressLine nvarchar(50));
CREATE USER ClerkR WITHOUT LOGIN;
GRANT VIEW DEFINITION ON TYPE::Customer.Address TO ClerkR;
REVOKE VIEW DEFINITION ON TYPE::Customer.Address FROM ClerkR CASCADE;
WITH TempUsers AS (
    SELECT 'ClerkR' AS UserName
)
SELECT * FROM TempUsers;
-- REMORPH CLEANUP: DROP TYPE Customer.Address;
-- REMORPH CLEANUP: DROP USER ClerkR;
