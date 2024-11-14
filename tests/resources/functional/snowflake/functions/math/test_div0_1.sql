
-- snowflake sql:
SELECT DIV0(a, b);

-- databricks sql:
select if ( b = 0 and a is not null, 0, a / b );
