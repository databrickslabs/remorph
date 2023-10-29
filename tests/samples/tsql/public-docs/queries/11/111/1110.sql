-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-remote-table-as-select-parallel-data-warehouse?view=aps-pdw-2016-au7

CREATE REMOTE TABLE OrderReporting.Orders.MyOrdersTable  
AT ( 'Data Source = SQLA, 1433; User ID = David; Password = e4n8@3;' )  
AS SELECT <select_criteria>;