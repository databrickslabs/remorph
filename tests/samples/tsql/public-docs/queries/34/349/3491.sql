-- see https://learn.microsoft.com/en-us/sql/t-sql/lesson-2-configuring-permissions-on-database-objects?view=sql-server-ver16

USE [TestData];
GO

CREATE USER [Mary] FOR LOGIN [computer_name\Mary];
GO