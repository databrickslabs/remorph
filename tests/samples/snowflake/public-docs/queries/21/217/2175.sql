-- see https://docs.snowflake.com/en/sql-reference/operators-arithmetic

select 2 n1, 7 n2, n1 / n2;


select 10.1 n1, 2.1 n2, n1 / n2;


select 10.001 n1, .001 n2, n1 / n2;


select .1 n1, .0000000000001 n2, n1 / n2;
