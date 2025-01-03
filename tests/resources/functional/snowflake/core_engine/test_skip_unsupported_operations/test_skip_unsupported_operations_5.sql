
-- snowflake sql:
CREATE STREAM mystream ON TABLE mytable;

-- databricks sql:
/* The following issues were detected:

   CREATE STREAM UNSUPPORTED
    CREATE STREAM mystream ON TABLE mytable
 */
