-- Unconditional multi-table insert
INSERT [ OVERWRITE ] ALL
  intoClause [ ... ]
<subquery>

-- Conditional multi-table insert
INSERT [ OVERWRITE ] { FIRST | ALL }
  { WHEN <condition> THEN intoClause [ ... ] }
  [ ... ]
  [ ELSE intoClause ]
<subquery>