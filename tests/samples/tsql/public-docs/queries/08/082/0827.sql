-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/bulk-insert-transact-sql?view=sql-server-ver16

BULK INSERT bulktest.dbo.t_float
FROM 'C:\t_float-c.dat' WITH (FORMATFILE = 'C:\t_floatformat-c-xml.xml');