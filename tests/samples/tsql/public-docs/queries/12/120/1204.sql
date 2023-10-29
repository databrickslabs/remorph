-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-azure-sql-data-warehouse?view=aps-pdw-2016-au7

CREATE TABLE Lineitem  
WITH (DISTRIBUTION = ROUND_ROBIN, CLUSTERED COLUMNSTORE INDEX ORDER(SHIPDATE))  
AS  
SELECT * FROM ext_Lineitem