-- see https://docs.snowflake.com/en/sql-reference/functions/ascii

SELECT column1, ASCII(column1)
  FROM (values('!'), ('A'), ('a'), ('bcd'), (''), (null));