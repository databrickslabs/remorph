
-- snowflake sql:
select to_char ( current_timestamp ( ) ,'yyyymmdd' )

-- databricks sql:
SELECT
    TO_CHAR(CURRENT_TIMESTAMP(), 'yyyyMMdd')
