
-- snowflake sql:
ALTER STREAM mystream SET COMMENT = 'New comment for stream';

-- databricks sql:
/* The following issues were detected:

   Unknown ALTER command variant
    ALTER STREAM mystream SET COMMENT = 'New comment for stream'
 */
