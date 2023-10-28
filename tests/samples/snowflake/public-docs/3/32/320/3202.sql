ALTER DYNAMIC TABLE [ <name> ] { SUSPEND | RESUME }

ALTER DYNAMIC TABLE [ <name> ] REFRESH

ALTER DYNAMIC TABLE <name> SET
  [ TARGET_LAG = { '<num> { seconds | minutes | hours | days }'  | DOWNSTREAM } ]
  [ WAREHOUSE = <warehouse_name> ]