-- snowflake sql:

SELECT REGEXP_SUBSTR('The real world of The Doors', 'The\\W+\\w+', 1, 2);

-- databricks sql:

SELECT REGEXP_EXTRACT_ALL(SUBSTR('The real world of The Doors', 1), 'The\\W+\\w+', 0)[1];
