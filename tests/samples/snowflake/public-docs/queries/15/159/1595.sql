-- see https://docs.snowflake.com/en/sql-reference/functions/unicode

SELECT column1, UNICODE(column1), CHAR(UNICODE(column1))
FROM values('a'), ('\u2744'), ('cde'), (''), (null);
