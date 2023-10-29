-- see https://docs.snowflake.com/en/sql-reference/functions/editdistance

SELECT s, t, EDITDISTANCE(s, t), EDITDISTANCE(t, s), EDITDISTANCE(s, t, 3), EDITDISTANCE(s, t, -1) FROM ed;
