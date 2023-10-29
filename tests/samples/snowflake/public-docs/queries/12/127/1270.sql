-- see https://docs.snowflake.com/en/sql-reference/functions/object_construct_keep_null

SELECT OBJECT_CONSTRUCT('key_1', 'one', 'key_2', NULL) AS WITHOUT_KEEP_NULL,
       OBJECT_CONSTRUCT_KEEP_NULL('key_1', 'one', 'key_2', NULL) AS KEEP_NULL_1,
       OBJECT_CONSTRUCT_KEEP_NULL('key_1', 'one', NULL, 'two') AS KEEP_NULL_2
       ;