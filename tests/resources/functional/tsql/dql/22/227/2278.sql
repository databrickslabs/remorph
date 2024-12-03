--Query type: DQL
WITH options AS (SELECT CAST(0 AS INT) AS options_value)
SELECT GET_BIT(options.options_value, 0) AS [DISABLE_DEF_CNST_CHK],
       GET_BIT(options.options_value, 1) AS [IMPLICIT_TRANSACTIONS],
       GET_BIT(options.options_value, 2) AS [CURSOR_CLOSE_ON_COMMIT],
       GET_BIT(options.options_value, 3) AS [ANSI_WARNINGS],
       GET_BIT(options.options_value, 4) AS [ANSI_PADDING],
       GET_BIT(options.options_value, 5) AS [ANSI_NULLS],
       GET_BIT(options.options_value, 6) AS [ARITHABORT],
       GET_BIT(options.options_value, 7) AS [ARITHIGNORE],
       GET_BIT(options.options_value, 8) AS [QUOTED_IDENTIFIER],
       GET_BIT(options.options_value, 9) AS [NOCOUNT],
       GET_BIT(options.options_value, 10) AS [ANSI_NULL_DFLT_ON],
       GET_BIT(options.options_value, 11) AS [ANSI_NULL_DFLT_OFF],
       GET_BIT(options.options_value, 12) AS [CONCAT_NULL_YIELDS_NULL],
       GET_BIT(options.options_value, 13) AS [NUMERIC_ROUNDABORT],
       GET_BIT(options.options_value, 14) AS [XACT_ABORT]
FROM options
