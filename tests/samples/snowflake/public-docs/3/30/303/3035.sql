CREATE [ OR REPLACE ] { DATABASE | SCHEMA | TABLE } [ IF NOT EXISTS ] <object_name>
  CLONE <source_object_name>
        [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
  ...