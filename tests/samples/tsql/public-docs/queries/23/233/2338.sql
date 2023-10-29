-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/opendatasource-transact-sql?view=sql-server-ver16

SELECT * FROM OPENDATASOURCE('Microsoft.Jet.OLEDB.4.0',  
    'Data Source=C:\DataFolder\Documents\TestExcel.xls;Extended Properties=EXCEL 5.0')...[Sheet1$] ;