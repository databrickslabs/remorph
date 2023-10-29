-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-as-select-azure-sql-data-warehouse?view=aps-pdw-2016-au7

SELECT *
INTO    #tmp_fct
FROM    [dbo].[FactInternetSales]