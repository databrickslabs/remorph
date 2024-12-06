-- snowflake sql:

SELECT REGEXP_SUBSTR('The real world of The Doors', 'the\\W+\\w+', 1, 2, 'i');

-- databricks sql:

SELECT REGEXP_EXTRACT_ALL(SUBSTR('The real world of The Doors', 1), '(?i)the\\W+\\w+', 0)[1];
