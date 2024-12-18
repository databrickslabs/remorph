-- tsql sql:
SELECT COL_LENGTH('customer', 'c_name') AS 'VarChar', COL_LENGTH('customer', 'c_address') AS 'NVarChar' FROM (VALUES ('customer', 'c_name', 'c_address')) AS temp_table(table_name, column_name, column_name2);
