CREATE TABLE <table_name> ( <col1> <data_type> [ WITH ] MASKING POLICY <policy_name> [ , ... ] )
  ...
  [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col1> [ , ... ] )
  AS SELECT <query>
  [ ... ]