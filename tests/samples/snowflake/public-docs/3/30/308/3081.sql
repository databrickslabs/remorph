ALTER MATERIALIZED VIEW <name>
  {
  RENAME TO <new_name>                     |
  CLUSTER BY ( <expr1> [, <expr2> ... ] )  |
  DROP CLUSTERING KEY                      |
  SUSPEND RECLUSTER                        |
  RESUME RECLUSTER                         |
  SUSPEND                                  |
  RESUME                                   |
  SET {
    [ SECURE ]
    [ COMMENT = '<comment>' ]
    }                                      |
  UNSET {
    SECURE                                 |
    COMMENT
    }
  }