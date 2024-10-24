
-- snowflake sql:
ALTER SESSION SET QUERY_TAG = 'tag1';

-- databricks sql:
/* The following issues were detected:

   Unknown ALTER command variant
    ALTER SESSION SET QUERY_TAG = 'tag1'
 */
