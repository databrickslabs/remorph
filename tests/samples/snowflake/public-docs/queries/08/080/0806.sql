-- see https://docs.snowflake.com/en/sql-reference/functions/between

SELECT 'm' BETWEEN COLLATE('A', 'lower') AND COLLATE('Z', 'lower');
SELECT COLLATE('m', 'upper') BETWEEN 'A' AND 'Z';