-- see https://learn.microsoft.com/en-us/sql/t-sql/lesson-2-configuring-permissions-on-database-objects?view=sql-server-ver16

CREATE LOGIN [computer_name\Mary]
    FROM WINDOWS
    WITH DEFAULT_DATABASE = [TestData];
GO