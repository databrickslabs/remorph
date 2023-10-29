-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showspaceused-transact-sql?view=aps-pdw-2016-au7

-- Uses AdventureWorks2022

DBCC PDW_SHOWSPACEUSED ( "AdventureWorksPDW2012.dbo.FactInternetSales" );
DBCC PDW_SHOWSPACEUSED ( "AdventureWorksPDW2012..FactInternetSales" );
DBCC PDW_SHOWSPACEUSED ( "dbo.FactInternetSales" );
DBCC PDW_SHOWSPACEUSED ( FactInternetSales );