-- see https://docs.snowflake.com/en/sql-reference/account-usage/access_history

UPDATE mydb.s1.t1 FROM mydb.s2.t2 SET t1.col1 = t2.col1;