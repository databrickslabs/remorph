-- see https://docs.snowflake.com/en/sql-reference/constructs/values

SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three'));


SELECT column1, $2 FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three'));
