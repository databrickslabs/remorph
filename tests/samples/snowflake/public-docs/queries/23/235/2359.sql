-- see https://docs.snowflake.com/en/sql-reference/data-type-conversion

select system$typeof(ifnull(12.3, 0)),
       system$typeof(ifnull(NULL, 0));
