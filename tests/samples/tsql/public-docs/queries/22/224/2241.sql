-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/raiserror-transact-sql?view=sql-server-ver16

RAISERROR (N'<\<%*.*s>>', -- Message text.
           10, -- Severity,
           1, -- State,
           7, -- First argument used for width.
           3, -- Second argument used for precision.
           N'abcde'); -- Third argument supplies the string.
-- The message text returned is: <<    abc>>.
GO
RAISERROR (N'<\<%7.3s>>', -- Message text.
           10, -- Severity,
           1, -- State,
           N'abcde'); -- First argument supplies the string.
-- The message text returned is: <<    abc>>.
GO