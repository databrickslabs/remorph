-- snowflake sql:

SELECT REGEXP_SUBSTR('The real world of The Doors', 'The\\W+\\w+', 2);

-- databricks sql:

SELECT REGEXP_EXTRACT(SUBSTR('The real world of The Doors', 2), 'The\\W+\\w+', 0);
