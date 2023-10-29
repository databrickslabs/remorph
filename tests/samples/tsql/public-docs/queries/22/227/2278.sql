-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/options-transact-sql?view=sql-server-ver16

SELECT
      GET_BIT(@@OPTIONS, 0)  /* 1     */ AS [DISABLE_DEF_CNST_CHK] -- Controls interim or deferred constraint checking.
    , GET_BIT(@@OPTIONS, 1)  /* 2     */ AS [IMPLICIT_TRANSACTIONS] -- For dblib network library connections, controls whether a transaction is started implicitly when a statement is executed. The IMPLICIT_TRANSACTIONS setting has no effect on ODBC or OLEDB connections.
    , GET_BIT(@@OPTIONS, 2)  /* 4     */ AS [CURSOR_CLOSE_ON_COMMIT] -- Controls behavior of cursors after a commit operation has been performed.
    , GET_BIT(@@OPTIONS, 3)  /* 8     */ AS [ANSI_WARNINGS] -- Controls truncation and NULL in aggregate warnings.
    , GET_BIT(@@OPTIONS, 4)  /* 16    */ AS [ANSI_PADDING] -- Controls padding of fixed-length variables.
    , GET_BIT(@@OPTIONS, 5)  /* 32    */ AS [ANSI_NULLS] -- Controls NULL handling when using equality operators.
    , GET_BIT(@@OPTIONS, 6)  /* 64    */ AS [ARITHABORT] -- Terminates a query when an overflow or divide-by-zero error occurs during query execution.
    , GET_BIT(@@OPTIONS, 7)  /* 128   */ AS [ARITHIGNORE] -- Returns NULL when an overflow or divide-by-zero error occurs during a query.
    , GET_BIT(@@OPTIONS, 8)  /* 256   */ AS [QUOTED_IDENTIFIER] -- Differentiates between single and double quotation marks when evaluating an expression.
    , GET_BIT(@@OPTIONS, 9)  /* 512   */ AS [NOCOUNT] -- Turns off the message returned at the end of each statement that states how many rows were affected.
    , GET_BIT(@@OPTIONS, 10) /* 1024  */ AS [ANSI_NULL_DFLT_ON] -- Alters the session's behavior to use ANSI compatibility for nullability. New columns defined without explicit nullability are defined to allow nulls.
    , GET_BIT(@@OPTIONS, 11) /* 2048  */ AS [ANSI_NULL_DFLT_OFF] -- Alters the session's behavior not to use ANSI compatibility for nullability. New columns defined without explicit nullability do not allow nulls.
    , GET_BIT(@@OPTIONS, 12) /* 4096  */ AS [CONCAT_NULL_YIELDS_NULL] -- Returns NULL when concatenating a NULL value with a string.
    , GET_BIT(@@OPTIONS, 13) /* 8192  */ AS [NUMERIC_ROUNDABORT] -- Generates an error when a loss of precision occurs in an expression.
    , GET_BIT(@@OPTIONS, 14) /* 16384 */ AS [XACT_ABORT] -- Rolls back a transaction if a Transact-SQL statement raises a run-time error.*/
GO