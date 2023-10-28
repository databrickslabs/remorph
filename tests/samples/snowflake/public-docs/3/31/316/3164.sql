-- Partitions computed from expressions
CREATE [ OR REPLACE ] EXTERNAL TABLE [IF NOT EXISTS]
  <table_name>
    ( [ <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ]
      [ inlineConstraint ]
      [ , <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ... ]
      [ , ... ] )
  cloudProviderParams
  [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
  [ WITH ] LOCATION = externalStage
  [ REFRESH_ON_CREATE =  { TRUE | FALSE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ PATTERN = '<regex_pattern>' ]
  FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] } )
  [ AWS_SNS_TOPIC = '<string>' ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON (VALUE) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]

-- Partitions added and removed manually
CREATE [ OR REPLACE ] EXTERNAL TABLE [IF NOT EXISTS]
  <table_name>
    ( [ <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ]
      [ inlineConstraint ]
      [ , <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ... ]
      [ , ... ] )
  cloudProviderParams
  [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
  [ WITH ] LOCATION = externalStage
  PARTITION_TYPE = USER_SPECIFIED
  FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] } )
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON (VALUE) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]

-- Delta Lake
CREATE [ OR REPLACE ] EXTERNAL TABLE [IF NOT EXISTS]
  <table_name>
    ( [ <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ]
      [ inlineConstraint ]
      [ , <col_name> <col_type> AS <expr> | <part_col_name> <col_type> AS <part_expr> ... ]
      [ , ... ] )
  cloudProviderParams
  [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
  [ WITH ] LOCATION = externalStage
  PARTITION_TYPE = USER_SPECIFIED
  FILE_FORMAT = ( { FORMAT_NAME = '<file_format_name>' | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] } )
  [ TABLE_FORMAT = DELTA ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON (VALUE) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]