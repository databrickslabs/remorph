--Query type: DML
WITH StatusTable AS ( SELECT 'Success' AS Status, 'Package Loaded' AS Value ) SELECT Status, Value FROM StatusTable