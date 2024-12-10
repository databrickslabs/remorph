-- tsql sql:
WITH SupplierBinding AS ( SELECT 'SupplierBinding' AS Name, '//Supplier-Company.com/services/SupplierService' AS ServiceUrl, 'SupplierUser' AS UserName ) SELECT * FROM SupplierBinding
