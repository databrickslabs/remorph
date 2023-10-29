-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/options-transact-sql?view=sql-server-ver16

SELECT S.Bits,
    Flags.*
FROM (
    SELECT optRef,
        posRef,
        flagCheck
    FROM (
        SELECT ones.n + tens.n * 10
        FROM ( VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9) ) ones(n),
            ( VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9) ) tens(n)
        ) f1(powRef)
    CROSS APPLY (
        SELECT POWER(2, powRef)
        WHERE powRef <= 16
        ) f2(binRef)
    CROSS JOIN (
        VALUES (@@OPTIONS)
        ) f3(optRef)
    CROSS APPLY (
        SELECT (optRef & binRef) / binRef
        ) f4(flagRef)
    CROSS APPLY (
        SELECT RIGHT(CONVERT(VARCHAR(2), CAST(powRef AS VARBINARY(1)), 2), 1) [posRef],
            CAST(flagRef AS INT) [flagCheck]
        ) pref
    ) TP
PIVOT( MAX( flagCheck ) FOR posRef IN ( [0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [A], [B], [C], [D], [E], [F] )) P
CROSS APPLY (
    SELECT CONCAT ( '', [0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [A], [B], [C], [D], [E], [F] ),
        CONCAT ( '', [F], [E], [D], [C], [B], [A], [9], [8], [7], [6], [5], [4], [3], [2], [1], [0] )
    ) S (stib, Bits)
CROSS APPLY (
    SELECT
          CAST(P.[0] AS BIT) /* 1     */ [DISABLE_DEF_CNST_CHK] -- Controls interim or deferred constraint checking.
        , CAST(P.[1] AS BIT) /* 2     */ [IMPLICIT_TRANSACTIONS] -- For dblib network library connections, controls whether a transaction is started implicitly when a statement is executed. The IMPLICIT_TRANSACTIONS setting has no effect on ODBC or OLEDB connections.
        , CAST(P.[2] AS BIT) /* 4     */ [CURSOR_CLOSE_ON_COMMIT] -- Controls behavior of cursors after a commit operation has been performed.
        , CAST(P.[3] AS BIT) /* 8     */ [ANSI_WARNINGS] -- Controls truncation and NULL in aggregate warnings.
        , CAST(P.[4] AS BIT) /* 16    */ [ANSI_PADDING] -- Controls padding of fixed-length variables.
        , CAST(P.[5] AS BIT) /* 32    */ [ANSI_NULLS] -- Controls NULL handling when using equality operators.
        , CAST(P.[6] AS BIT) /* 64    */ [ARITHABORT] -- Terminates a query when an overflow or divide-by-zero error occurs during query execution.
        , CAST(P.[7] AS BIT) /* 128   */ [ARITHIGNORE] -- Returns NULL when an overflow or divide-by-zero error occurs during a query.
        , CAST(P.[8] AS BIT) /* 256   */ [QUOTED_IDENTIFIER] -- Differentiates between single and double quotation marks when evaluating an expression.
        , CAST(P.[9] AS BIT) /* 512   */ [NOCOUNT] -- Turns off the message returned at the end of each statement that states how many rows were affected.
        , CAST(P.[A] AS BIT) /* 1024  */ [ANSI_NULL_DFLT_ON] -- Alters the session's behavior to use ANSI compatibility for nullability. New columns defined without explicit nullability are defined to allow nulls.
        , CAST(P.[B] AS BIT) /* 2048  */ [ANSI_NULL_DFLT_OFF] -- Alters the session's behavior not to use ANSI compatibility for nullability. New columns defined without explicit nullability do not allow nulls.
        , CAST(P.[C] AS BIT) /* 4096  */ [CONCAT_NULL_YIELDS_NULL] -- Returns NULL when concatenating a NULL value with a string.
        , CAST(P.[D] AS BIT) /* 8192  */ [NUMERIC_ROUNDABORT] -- Generates an error when a loss of precision occurs in an expression.
        , CAST(P.[E] AS BIT) /* 16384 */ [XACT_ABORT] -- Rolls back a transaction if a Transact-SQL statement raises a run-time error.*/
    ) AS Flags;