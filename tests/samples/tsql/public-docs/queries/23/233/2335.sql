-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/create-diagnostics-session-transact-sql?view=aps-pdw-2016-au7

SELECT *   
FROM master.sysdiag.PdwOptimizationDiagnostics   
ORDER BY DateTimePublished;