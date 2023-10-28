CREATE [ OR REPLACE ] DYNAMIC TABLE <name>
  TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
  WAREHOUSE = <warehouse_name>
  AS <query>
  [ COMMENT = '<string_literal>' ]