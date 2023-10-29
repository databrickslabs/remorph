-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/raiserror-transact-sql?view=sql-server-ver16

EXEC sp_addmessage @msgnum = 50005,
              @severity = 10,
              @msgtext = N'<\<%7.3s>>';
GO
RAISERROR (50005, -- Message id.
           10, -- Severity,
           1, -- State,
           N'abcde'); -- First argument supplies the string.
-- The message text returned is: <<    abc>>.
GO
EXEC sp_dropmessage @msgnum = 50005;
GO