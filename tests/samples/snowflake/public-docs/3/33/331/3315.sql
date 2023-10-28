CREATE [ OR REPLACE ] TABLE <name> CLONE <source_table>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
  [ COPY GRANTS ]
  [ ... ]