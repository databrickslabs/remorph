-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showpartitionstats-transact-sql?view=aps-pdw-2016-au7

DBCC PDW_SHOWPARTITIONSTATS ("ssawPDW.dbo.FactInternetSales");
DBCC PDW_SHOWPARTITIONSTATS ("dbo.FactInternetSales");
DBCC PDW_SHOWPARTITIONSTATS (FactInternetSales);