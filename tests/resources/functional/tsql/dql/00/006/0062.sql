--Query type: DQL
WITH temp_result AS ( SELECT * FROM dbo.get_supplier_references('Supplier#000000001', 'UNITED STATES', 'AMERICA') ) SELECT * FROM temp_result;