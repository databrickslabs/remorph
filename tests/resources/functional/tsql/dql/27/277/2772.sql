--Query type: DQL
WITH CustomerCTE AS (SELECT 'London\Workstation1' AS CustomerName)
SELECT SUSER_SID(CustomerName) AS CustomerSID
FROM CustomerCTE;
