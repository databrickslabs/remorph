-- snowflake sql:
select id, string1,
       regexp_substr(string1, 'the\\W+\\w+') as "SUBSTRING"
    from demo2;

-- databricks sql:

select id, string1,
	   REGEXP_EXTRACT(string1, 'the\\W+\\w+', 0) as `SUBSTRING`
    from demo2;
