-- see https://docs.snowflake.com/en/sql-reference/constructs/limit

select c1 from testtable;


select c1 from testtable limit 3 offset 3;


select c1 from testtable order by c1;


select c1 from testtable order by c1 limit 3 offset 3;
