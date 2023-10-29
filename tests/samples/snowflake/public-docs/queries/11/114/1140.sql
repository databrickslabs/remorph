-- see https://docs.snowflake.com/en/sql-reference/functions/editdistance

SELECT EDITDISTANCE('future', 'past', 2) < 2;
