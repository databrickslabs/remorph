BULK INSERT Sales.Invoices
FROM '\\share\invoices\inv-2016-07-25.csv'
WITH (FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ';'
      , ROWTERMINATOR = '0x0a');