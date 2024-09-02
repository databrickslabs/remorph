--Query type: DQL
WITH TempResult AS ( SELECT * FROM ( VALUES (1, 'John'), (2, 'Jane') ) AS Customer (CustomerID, CustomerName) ) SELECT * INTO [dbo].[CustomerTemp] ON FG2 FROM TempResult