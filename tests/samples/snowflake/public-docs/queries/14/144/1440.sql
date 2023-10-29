-- see https://docs.snowflake.com/en/sql-reference/functions/system_last_change_commit_time

SELECT SYSTEM$LAST_CHANGE_COMMIT_TIME('mytable');


INSERT INTO mytable VALUES (2,100), (3,300);

SELECT SYSTEM$LAST_CHANGE_COMMIT_TIME('mytable');
