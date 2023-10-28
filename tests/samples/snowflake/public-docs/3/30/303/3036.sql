CREATE [ OR REPLACE ] { ALERT | FILE FORMAT | SEQUENCE | STAGE | STREAM | TASK }
  [ IF NOT EXISTS ] <object_name>
  CLONE <source_object_name>
  ...